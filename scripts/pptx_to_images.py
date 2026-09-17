"""
pptx_to_images.py
==================
把 .pptx 轉成逐頁 .png 圖片，供步驟 4 的視覺校對使用。

做法：pptx -> pdf（LibreOffice headless，最穩定的一段）-> 逐頁 png（PyMuPDF）。
不要嘗試讓 LibreOffice 直接吐出多張圖片，不同版本行為不一致（有時只給第一頁、
有時檔名規則不同），先轉成 pdf 這個中繼格式最可靠。

依賴：
    系統需安裝 libreoffice（soffice 指令可用）
    pip install pymupdf

用法：
    python pptx_to_images.py deck.pptx out_dir/ [--dpi 150]
"""

import argparse
import os
import subprocess
import sys


def convert_to_pdf(pptx_path: str, out_dir: str) -> str:
    os.makedirs(out_dir, exist_ok=True)
    cmd = [
        "soffice", "--headless", "--norestore",
        "--convert-to", "pdf", "--outdir", out_dir, pptx_path,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if result.returncode != 0:
        raise RuntimeError(
            f"LibreOffice 轉換失敗 (returncode={result.returncode}):\n"
            f"stdout: {result.stdout}\nstderr: {result.stderr}\n"
            "請確認 hermes 環境已安裝 libreoffice，且 pptx 路徑正確。"
        )

    base = os.path.splitext(os.path.basename(pptx_path))[0]
    pdf_path = os.path.join(out_dir, f"{base}.pdf")
    if not os.path.exists(pdf_path):
        raise RuntimeError(f"預期輸出 {pdf_path} 不存在，LibreOffice 可能用了不同檔名，"
                            f"請檢查 {out_dir} 目錄實際內容。")
    return pdf_path


def pdf_to_pngs(pdf_path: str, out_dir: str, dpi: int = 150) -> list:
    import fitz  # PyMuPDF

    doc = fitz.open(pdf_path)
    zoom = dpi / 72
    matrix = fitz.Matrix(zoom, zoom)
    paths = []
    for page_index in range(len(doc)):
        page = doc[page_index]
        pix = page.get_pixmap(matrix=matrix)
        out_path = os.path.join(out_dir, f"slide_{page_index + 1:03d}.png")
        pix.save(out_path)
        paths.append(out_path)
    return paths


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("pptx_path")
    parser.add_argument("out_dir")
    parser.add_argument("--dpi", type=int, default=150)
    args = parser.parse_args()

    pdf_path = convert_to_pdf(args.pptx_path, args.out_dir)
    png_paths = pdf_to_pngs(pdf_path, args.out_dir, dpi=args.dpi)

    print(f"共產出 {len(png_paths)} 張投影片圖片：")
    for p in png_paths:
        print(f"  {p}")


if __name__ == "__main__":
    main()
