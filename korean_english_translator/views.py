from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from anthropic import Anthropic
from django.conf import settings
from django.http import JsonResponse

# Initialize Anthropic client
anthropic = Anthropic(api_key=settings.ANTHROPIC_API_KEY)


class TranslateAPIView(APIView):
    def post(self, request):
        try:
            # Get required parameters from request
            text = request.data.get("text")
            from_lang = request.data.get("from")
            to_lang = request.data.get("to")

            if not all([text, from_lang, to_lang]):
                return Response(
                    {"error": "Missing required parameters"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Create translation prompt
            prompt = f"""
            You are a professional translator. Your task is to translate the following text 
            from {from_lang.upper()} to {to_lang.upper()}:

            {text}

            Instructions:
            1. Return ONLY the translated text in {to_lang.upper()}
            2. Include pronunciation guide in parentheses after each word:
               - For English: Use IPA (International Phonetic Alphabet) in parentheses
               - For Korean: Use Hangul phonetic spelling in parentheses
            3. Format the pronunciation guide as: (word) [pronunciation]
            4. For each word, provide:
               - Example usage in a phrase or sentence
               - Cultural context (if applicable):
                 * For Korean words: indicate if it's native Korean or Sino-Korean
                 * For slang terms: mark them as such
                 * For similar words: provide alternatives
            5. For Korean phrases with formality markers (요, ㅂ니다, etc.), analyze and break down:
               - Formality level (low, medium, high)
               - Context of use (formal setting, casual conversation, etc.)
               - Alternative forms (if applicable)
               - Example usage in different formality levels
            6. Format the output as:
               (word) [pronunciation] - Example usage: [sentence] - [context/notes]
               For phrases: [phrase] [pronunciation] - Formality: [level] - Context: [description] - Alternative forms: [list]
            7. Do not include any explanations, introductions, or additional text
            8. Maintain the original meaning and tone
            9. Format the output exactly as the input

            Translation:
            """

            # Call Anthropic API
            response = anthropic.messages.create(
                model="claude-opus-4-20250514",
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}],
            )

            # Extract and return the translation
            translation = response.content[0].text
            return Response({"translation": translation}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PhraseLookupAPIView(APIView):
    def post(self, request):
        try:
            # Get required parameter
            phrase = request.data.get("phrase")
            
            if not phrase:
                return Response(
                    {"error": "Missing required parameter: phrase"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Create phrase analysis prompt
            prompt = f"""
            You are a Korean language expert. Analyze the following Korean phrase:
            {phrase}

            Please provide:
            1. Pronunciation: Use Hangul phonetic spelling in parentheses
            2. Word origin: Is it native Korean or Sino-Korean?
            3. Example usage in a sentence
            4. Cultural context:
               - Common usage scenarios
               - Any cultural significance
               - Slang or formal usage
            5. Formality level:
               - Low (casual conversation)
               - Medium (neutral/formal conversation)
               - High (business/formal settings)
            6. Alternative forms:
               - Different formality variations
               - Regional variations
               - Common misspellings

            Format the response as JSON ONLY. Do not include any additional text or explanations.
            {{
                "phrase": "{phrase}",
                "pronunciation": "[phonetic spelling]",
                "origin": "native/Sino-Korean",
                "example": "Example sentence",
                "context": "Cultural context",
                "formality": {{
                    "level": "low/medium/high",
                    "alternatives": ["alternative forms"]
                }}
            }}
            """

            # Call Anthropic API
            response = anthropic.messages.create(
                model="claude-opus-4-20250514",
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}],
            )

            # Extract and clean up the word analysis
            analysis = response.content[0].text
            # Remove markdown formatting and backticks
            analysis = analysis.replace('```json', '').replace('```', '').strip()
            # Remove any text before or after the JSON
            analysis = analysis.strip()
            if analysis.startswith('{') and analysis.endswith('}'):  # Ensure it's a JSON object
                analysis = analysis
            else:
                # Find the JSON object within the text
                start = analysis.find('{')
                end = analysis.rfind('}')
                if start != -1 and end != -1:
                    analysis = analysis[start:end+1]
            print(analysis)
            return Response({"analysis": analysis}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
