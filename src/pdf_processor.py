import PyPDF2
import pdfplumber
import os
from typing import Optional

class PDFProcessor:
    """Class to handle PDF text extraction and processing."""
    
    def __init__(self, pdf_path: str):
        """
        Initialize the PDF processor.
        
        Args:
            pdf_path (str): Path to the PDF file
        """
        self.pdf_path = pdf_path
        self.text_content = ""
        self.is_loaded = False
    
    def extract_text_pypdf2(self) -> str:
        """
        Extract text using PyPDF2 library.
        
        Returns:
            str: Extracted text content
        """
        try:
            with open(self.pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                return text
        except Exception as e:
            print(f"Error extracting text with PyPDF2: {e}")
            return ""
    
    def extract_text_pdfplumber(self) -> str:
        """
        Extract text using pdfplumber library (often better for complex layouts).
        
        Returns:
            str: Extracted text content
        """
        try:
            text = ""
            with pdfplumber.open(self.pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            return text
        except Exception as e:
            print(f"Error extracting text with pdfplumber: {e}")
            return ""
    
    def extract_text(self, method: str = "pdfplumber") -> str:
        """
        Extract text from PDF using specified method.
        
        Args:
            method (str): Method to use ('pdfplumber' or 'pypdf2')
            
        Returns:
            str: Extracted text content
        """
        if not os.path.exists(self.pdf_path):
            raise FileNotFoundError(f"PDF file not found: {self.pdf_path}")
        
        if method == "pdfplumber":
            self.text_content = self.extract_text_pdfplumber()
        else:
            self.text_content = self.extract_text_pypdf2()
        
        # If first method fails, try the other
        if not self.text_content.strip():
            print(f"First method failed, trying alternative...")
            if method == "pdfplumber":
                self.text_content = self.extract_text_pypdf2()
            else:
                self.text_content = self.extract_text_pdfplumber()
        
        self.is_loaded = True
        return self.text_content
    
    def get_text_chunks(self, chunk_size: int = 1000, overlap: int = 100) -> list:
        """
        Split text into chunks for better processing.
        
        Args:
            chunk_size (int): Size of each chunk
            overlap (int): Overlap between chunks
            
        Returns:
            list: List of text chunks
        """
        if not self.is_loaded:
            self.extract_text()
        
        chunks = []
        text = self.text_content
        
        for i in range(0, len(text), chunk_size - overlap):
            chunk = text[i:i + chunk_size]
            chunks.append(chunk)
            
        return chunks
    
    def get_summary_info(self) -> dict:
        """
        Get summary information about the PDF.
        
        Returns:
            dict: Summary information
        """
        if not self.is_loaded:
            self.extract_text()
        
        return {
            "file_path": self.pdf_path,
            "text_length": len(self.text_content),
            "word_count": len(self.text_content.split()),
            "is_loaded": self.is_loaded
        }
