import PyPDF2

pdf_path = "PDF/book- Approximation Algorithms.pdf"
output_file = "chapter3_content.txt"

try:
    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        with open(output_file, "w", encoding="utf-8") as out:
            # Extract PDF pages 45 to 70 (covering Chapter 3)
            # Chapter 3 title was found on page 47.
            start_page = 45
            end_page = 70
            
            for i in range(start_page, end_page + 1):
                if i < len(reader.pages):
                    page = reader.pages[i]
                    text = page.extract_text()
                    out.write(f"--- Page {i} ---\n")
                    out.write(text)
                    out.write("\n\n")
            print(f"Extracted pages {start_page}-{end_page} to {output_file}")

except Exception as e:
    print(f"Error: {e}")
