"""
Email Service for sending FIR drafts and legal documents.
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Optional
from app.config import (
    SMTP_SERVER,
    SMTP_PORT,
    SMTP_USERNAME,
    SMTP_PASSWORD,
    EMAIL_FROM,
    EMAIL_FROM_NAME
)

# Email libraries are built into Python, no additional imports needed


class EmailService:
    """
    Service for sending emails via SMTP.
    """
    
    def __init__(self):
        """
        Initialize the email service.
        """
        self.smtp_server = SMTP_SERVER
        self.smtp_port = SMTP_PORT
        self.smtp_username = SMTP_USERNAME
        self.smtp_password = SMTP_PASSWORD
        self.email_from = EMAIL_FROM
        self.email_from_name = EMAIL_FROM_NAME
    
    def _generate_fir_draft_html(self, roadmap: Dict, user_query: str, user_name: str = "User") -> str:
        """
        Generate HTML email content for FIR draft.
        
        Args:
            roadmap: Roadmap response dictionary
            user_query: User's original query
            user_name: User's name (optional)
        
        Returns:
            HTML string for email body
        """
        crime_type = roadmap.get("crime_type", "Legal Matter")
        immediate_actions = roadmap.get("immediate_actions", [])
        fir_steps = roadmap.get("fir_steps", [])
        evidence_to_preserve = roadmap.get("evidence_to_preserve", [])
        relevant_laws = roadmap.get("relevant_laws", [])
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .header {{
                    background-color: #2c3e50;
                    color: white;
                    padding: 20px;
                    border-radius: 5px;
                    margin-bottom: 20px;
                }}
                .section {{
                    margin-bottom: 25px;
                    padding: 15px;
                    background-color: #f8f9fa;
                    border-left: 4px solid #2c3e50;
                }}
                .section-title {{
                    font-size: 18px;
                    font-weight: bold;
                    color: #2c3e50;
                    margin-bottom: 10px;
                }}
                ul {{
                    margin: 10px 0;
                    padding-left: 20px;
                }}
                li {{
                    margin: 8px 0;
                }}
                .query-box {{
                    background-color: #e3f2fd;
                    padding: 15px;
                    border-radius: 5px;
                    margin-bottom: 20px;
                    border-left: 4px solid #2196f3;
                }}
                .footer {{
                    margin-top: 30px;
                    padding: 15px;
                    background-color: #f5f5f5;
                    border-radius: 5px;
                    font-size: 12px;
                    color: #666;
                }}
                .warning {{
                    background-color: #fff3cd;
                    border-left: 4px solid #ffc107;
                    padding: 15px;
                    margin: 20px 0;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>FIR Draft - Nyay Sahayak</h1>
                <p>Initial Action Roadmap for Your Legal Matter</p>
            </div>
            
            <div class="query-box">
                <strong>Your Query:</strong><br>
                {user_query}
            </div>
            
            <div class="section">
                <div class="section-title">🔍 Crime/Incident Type</div>
                <p><strong>{crime_type}</strong></p>
            </div>
            
            <div class="section">
                <div class="section-title">⚡ Immediate Actions</div>
                <ul>
        """
        
        for action in immediate_actions:
            html += f"                    <li>{action}</li>\n"
        
        html += """
                </ul>
            </div>
            
            <div class="section">
                <div class="section-title">📋 FIR Filing Steps</div>
                <ol>
        """
        
        for i, step in enumerate(fir_steps, 1):
            html += f"                    <li>{step}</li>\n"
        
        html += """
                </ol>
            </div>
            
            <div class="section">
                <div class="section-title">📎 Evidence to Preserve</div>
                <ul>
        """
        
        for evidence in evidence_to_preserve:
            html += f"                    <li>{evidence}</li>\n"
        
        html += """
                </ul>
            </div>
            
            <div class="section">
                <div class="section-title">⚖️ Relevant Laws</div>
                <ul>
        """
        
        for law in relevant_laws:
            html += f"                    <li>{law}</li>\n"
        
        html += """
                </ul>
            </div>
            
            <div class="warning">
                <strong>⚠️ Important Disclaimer:</strong><br>
                This is a draft FIR and legal guidance generated by AI. It is for informational purposes only 
                and should not be considered as legal advice. Please consult with a qualified lawyer before 
                taking any legal action. The information provided is based on general legal knowledge and 
                may not be applicable to your specific situation.
            </div>
            
            <div class="footer">
                <p><strong>Nyay Sahayak - Your AI Guide for Legal First Steps</strong></p>
                <p>This email was generated automatically. For legal assistance, please consult with a qualified lawyer.</p>
                <p>© 2025 Nyay Sahayak. All rights reserved.</p>
            </div>
        </body>
        </html>
        """
        
        return html
    
    def _generate_fir_draft_text(self, roadmap: Dict, user_query: str, user_name: str = "User") -> str:
        """
        Generate plain text email content for FIR draft.
        
        Args:
            roadmap: Roadmap response dictionary
            user_query: User's original query
            user_name: User's name (optional)
        
        Returns:
            Plain text string for email body
        """
        crime_type = roadmap.get("crime_type", "Legal Matter")
        immediate_actions = roadmap.get("immediate_actions", [])
        fir_steps = roadmap.get("fir_steps", [])
        evidence_to_preserve = roadmap.get("evidence_to_preserve", [])
        relevant_laws = roadmap.get("relevant_laws", [])
        
        text = f"""
FIR DRAFT - NYAY SAHAYAK
Initial Action Roadmap for Your Legal Matter

{'='*60}

YOUR QUERY:
{user_query}

{'='*60}

CRIME/INCIDENT TYPE:
{crime_type}

{'='*60}

IMMEDIATE ACTIONS:
"""
        for i, action in enumerate(immediate_actions, 1):
            text += f"{i}. {action}\n"
        
        text += f"\n{'='*60}\n\nFIR FILING STEPS:\n"
        for i, step in enumerate(fir_steps, 1):
            text += f"{i}. {step}\n"
        
        text += f"\n{'='*60}\n\nEVIDENCE TO PRESERVE:\n"
        for i, evidence in enumerate(evidence_to_preserve, 1):
            text += f"{i}. {evidence}\n"
        
        text += f"\n{'='*60}\n\nRELEVANT LAWS:\n"
        for i, law in enumerate(relevant_laws, 1):
            text += f"{i}. {law}\n"
        
        text += f"""
{'='*60}

IMPORTANT DISCLAIMER:
This is a draft FIR and legal guidance generated by AI. It is for informational 
purposes only and should not be considered as legal advice. Please consult with 
a qualified lawyer before taking any legal action.

{'='*60}

Nyay Sahayak - Your AI Guide for Legal First Steps
© 2025 Nyay Sahayak. All rights reserved.
"""
        
        return text
    
    def send_fir_draft(self, to_email: str, roadmap: Dict, user_query: str, user_name: Optional[str] = None) -> bool:
        """
        Send FIR draft email to the user.
        
        Args:
            to_email: Recipient email address
            roadmap: Roadmap response dictionary
            user_query: User's original query
            user_name: User's name (optional)
        
        Returns:
            True if email sent successfully, False otherwise
        
        Raises:
            ValueError: If email configuration is missing
            Exception: If email sending fails
        """
        if not self.smtp_username or not self.smtp_password:
            raise ValueError(
                "SMTP credentials not configured. Please set SMTP_USERNAME and SMTP_PASSWORD "
                "in your .env file or environment variables."
            )
        
        if not self.email_from:
            raise ValueError("EMAIL_FROM not configured. Please set it in your .env file.")
        
        # Create message
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"FIR Draft - {roadmap.get('crime_type', 'Legal Matter')} - Nyay Sahayak"
        msg["From"] = f"{self.email_from_name} <{self.email_from}>"
        msg["To"] = to_email
        
        # Create text and HTML versions
        text_content = self._generate_fir_draft_text(roadmap, user_query, user_name or "User")
        html_content = self._generate_fir_draft_html(roadmap, user_query, user_name or "User")
        
        # Attach parts
        part1 = MIMEText(text_content, "plain")
        part2 = MIMEText(html_content, "html")
        
        msg.attach(part1)
        msg.attach(part2)
        
        # Send email
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
            return True
        except Exception as e:
            raise Exception(f"Failed to send email: {str(e)}")


# Global email service instance
_email_service: Optional[EmailService] = None


def get_email_service() -> EmailService:
    """
    Get or create the global email service instance.
    
    Returns:
        EmailService instance
    """
    global _email_service
    if _email_service is None:
        _email_service = EmailService()
    return _email_service

