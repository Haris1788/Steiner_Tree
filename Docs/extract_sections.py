import PyPDF2
import os

pdf_path = "PDF/book- Approximation Algorithms.pdf"

try:
    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        num_pages = len(reader.pages)
        print(f"Total pages: {num_pages}")
        
        # Search for "Steiner Tree" in Vazirani to find the page
        print("Searching for 'Steiner Tree' in Vazirani...")
        found_count = 0
        for i in range(num_pages):
            page = reader.pages[i]
            text = page.extract_text()
            if "Steiner Tree" in text or "Steiner tree" in text:
                print(f"--- Found 'Steiner Tree' on Page {i} ---")
                print(text[:500]) # Print first 500 chars to see context
                print("\n")
                found_count += 1
                if found_count > 5: # Stop after finding a few mentions
                    break
except FileNotFoundError:
    print(f"File not found: {pdf_path}")
except Exception as e:
    print(f"Error: {e}")
