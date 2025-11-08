"""
Query Handler Service
Handles Gemini API calls and generates structured legal roadmaps.
"""

import json
import re
import asyncio
from typing import Dict, List, Optional
import google.generativeai as genai
from app.config import GOOGLE_API_KEY, GEMINI_MODEL
from app.services.rag_pipeline import get_rag_pipeline


class QueryHandler:
    """
    Handles user queries by combining RAG retrieval with Gemini generation.
    """
    
    def __init__(self):
        """
        Initialize the query handler with Gemini API.
        """
        if not GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY is not configured")
        
        genai.configure(api_key=GOOGLE_API_KEY)
        self.model = genai.GenerativeModel(GEMINI_MODEL)
        self.rag_pipeline = get_rag_pipeline()
    
    def _build_prompt(self, user_query: str, retrieved_chunks: List[Dict], city: Optional[str] = None, incident_type: Optional[str] = None) -> str:
        """
        Build the prompt for Gemini using user query and retrieved context.
        
        Args:
            user_query: User's original query
            retrieved_chunks: List of retrieved document chunks from RAG
        
        Returns:
            Formatted prompt string
        """
        # Combine retrieved chunks into context
        context_text = "\n\n---\n\n".join([
            f"Source: {chunk.get('meta', {}).get('source_name', 'Unknown')}\n"
            f"Content: {chunk.get('text', '')}"
            for chunk in retrieved_chunks
        ])
        # Include optional city and incident type to give the model extra context if available.
        extra_ctx = ""
        if city:
            extra_ctx += f"City: {city}\n"
        if incident_type:
            extra_ctx += f"Incident Type: {incident_type}\n"

        prompt = f"""You are "Nyay Sahayak", an empathetic legal AI assistant helping Indian citizens take their first legal steps after a crime or incident.

Analyze the following user situation and the provided legal texts from Indian Penal Code (IPC) and Information Technology Act.

{extra_ctx}
User Situation:
{user_query}

Relevant Legal Context:
{context_text}

Based on the user's situation and the legal context provided, identify:
1. Crime/incident type
2. Immediate actions the user should take
3. FIR filing process (step-by-step)
4. Evidence to preserve
5. Relevant IPC/IT Act sections

Return strictly in valid JSON format with these exact keys:
{{
  "crime_type": "<string>",
  "immediate_actions": ["<action1>", "<action2>", ...],
  "fir_steps": ["<step1>", "<step2>", ...],
  "evidence_to_preserve": ["<evidence1>", "<evidence2>", ...],
  "relevant_laws": ["<law1>", "<law2>", ...]
}}

Important:
- Be specific and actionable
- Use Indian legal terminology
- Include relevant IPC sections (e.g., "IPC 420 – Cheating")
- Include IT Act sections if applicable (e.g., "IT Act 66D – Impersonation")
- Provide clear, step-by-step FIR filing instructions
- Focus on immediate actions the user can take right now

Return ONLY the JSON object, no additional text or markdown formatting."""
        
        return prompt
    
    def _extract_json(self, text: str) -> Optional[Dict]:
        """
        Extract JSON from Gemini's response text.
        Handles cases where response may include markdown code blocks.
        
        Args:
            text: Raw response text from Gemini
        
        Returns:
            Parsed JSON dictionary or None if parsing fails
        """
        # Try to find JSON in markdown code blocks
        json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', text, re.DOTALL)
        if json_match:
            text = json_match.group(1)
        
        # Try to find JSON object directly
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            text = json_match.group(0)
        
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return None
    
    def _create_fallback_response(self, user_query: str) -> Dict:
        """
        Create a fallback response when Gemini fails or returns invalid JSON.
        
        Args:
            user_query: User's original query
        
        Returns:
            Fallback response dictionary
        """
        return {
            "crime_type": "Legal Matter",
            "immediate_actions": [
                "Document all details of the incident",
                "Preserve any evidence related to the incident",
                "Contact a local lawyer for legal advice"
            ],
            "fir_steps": [
                "Visit your nearest police station",
                "Provide a written complaint with all details",
                "Request a copy of the FIR after filing"
            ],
            "evidence_to_preserve": [
                "Any documents related to the incident",
                "Screenshots or photos if applicable",
                "Witness contact information"
            ],
            "relevant_laws": [
                "Consult with a legal expert for specific sections"
            ]
        }
    
    async def process_query(self, user_query: str, city: Optional[str] = None, incident_type: Optional[str] = None) -> Dict:
        """
        Process user query and generate structured legal roadmap.
        
        Args:
            user_query: User's description of the incident
        
        Returns:
            Dictionary containing structured roadmap response
        """
        try:
            # Retrieve relevant chunks using RAG with optional metadata filters
            retrieved_chunks = self.rag_pipeline.retrieve(
                user_query,
                city=city,
                incident_type=incident_type
            )

            # Build prompt with context (include city/incident_type clues if provided)
            prompt = self._build_prompt(user_query, retrieved_chunks, city, incident_type)
            
            # Generate response using Gemini (run in thread pool to avoid blocking)
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.model.generate_content(prompt)
            )
            response_text = response.text
            
            # Extract JSON from response
            result = self._extract_json(response_text)
            
            if result is None:
                # Fallback if JSON extraction fails
                print(f"Warning: Failed to extract JSON from Gemini response. Using fallback.")
                return self._create_fallback_response(user_query)
            
            # Validate required keys
            required_keys = ["crime_type", "immediate_actions", "fir_steps", 
                           "evidence_to_preserve", "relevant_laws"]
            for key in required_keys:
                if key not in result:
                    result[key] = []
                elif not isinstance(result[key], list) and key != "crime_type":
                    result[key] = [str(result[key])]
            
            return result
        
        except Exception as e:
            print(f"Error processing query: {e}")
            # Return fallback response on error
            return self._create_fallback_response(user_query)

