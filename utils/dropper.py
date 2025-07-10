def txt_to_pdf(txt_path, pdf_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    try:
        # Try to use DejaVu if it works
        font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
        if os.path.exists(font_path):
            pdf.add_font("DejaVu", "", font_path, uni=True)
            pdf.set_font("DejaVu", size=12)
        else:
            raise FileNotFoundError("DejaVu font not found.")
    except Exception as e:
        print(f"[⚠] Font load failed, using Courier: {e}")
        pdf.set_font("Courier", size=12)

    with open(txt_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                pdf.multi_cell(0, 10, line.strip())
            except Exception:
                # Fallback to encoding-safe characters
                pdf.multi_cell(0, 10, line.encode('latin-1', 'replace').decode('latin-1'))

    pdf.output(pdf_path)

