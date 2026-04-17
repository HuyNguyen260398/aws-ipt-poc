"""
Generate Vietnamese thesis proposal PDF for Nhiên's ITP bleeding prediction research.
Formal academic style suitable for submission to thesis committee.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
    KeepTogether, ListFlowable, ListItem
)
from reportlab.platypus.tableofcontents import TableOfContents

# Register Vietnamese-compatible fonts
pdfmetrics.registerFont(TTFont('DejaVu', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DejaVu-Bold', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))
pdfmetrics.registerFont(TTFont('DejaVu-Italic', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf'))
pdfmetrics.registerFont(TTFont('DejaVu-BoldItalic', '/usr/share/fonts/truetype/dejavu/DejaVuSans-BoldOblique.ttf'))
pdfmetrics.registerFont(TTFont('DejaVuSerif', '/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf'))
pdfmetrics.registerFont(TTFont('DejaVuSerif-Bold', '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'))

from reportlab.pdfbase.pdfmetrics import registerFontFamily
registerFontFamily('DejaVu',
                   normal='DejaVu',
                   bold='DejaVu-Bold',
                   italic='DejaVu-Italic',
                   boldItalic='DejaVu-BoldItalic')


# ============================================================
# STYLES
# ============================================================
styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    'VNTitle',
    parent=styles['Title'],
    fontName='DejaVu-Bold',
    fontSize=16,
    leading=22,
    alignment=TA_CENTER,
    spaceAfter=12,
    textColor=colors.HexColor('#1a365d'),
)

subtitle_style = ParagraphStyle(
    'VNSubtitle',
    parent=styles['Heading2'],
    fontName='DejaVu-Bold',
    fontSize=13,
    leading=18,
    alignment=TA_CENTER,
    spaceAfter=10,
    textColor=colors.HexColor('#2c5282'),
)

heading1_style = ParagraphStyle(
    'VNH1',
    parent=styles['Heading1'],
    fontName='DejaVu-Bold',
    fontSize=14,
    leading=20,
    spaceBefore=18,
    spaceAfter=10,
    textColor=colors.HexColor('#1a365d'),
    keepWithNext=True,
)

heading2_style = ParagraphStyle(
    'VNH2',
    parent=styles['Heading2'],
    fontName='DejaVu-Bold',
    fontSize=12,
    leading=16,
    spaceBefore=12,
    spaceAfter=8,
    textColor=colors.HexColor('#2c5282'),
    keepWithNext=True,
)

heading3_style = ParagraphStyle(
    'VNH3',
    parent=styles['Heading3'],
    fontName='DejaVu-Bold',
    fontSize=11,
    leading=14,
    spaceBefore=8,
    spaceAfter=6,
    textColor=colors.HexColor('#2d3748'),
    keepWithNext=True,
)

body_style = ParagraphStyle(
    'VNBody',
    parent=styles['Normal'],
    fontName='DejaVu',
    fontSize=11,
    leading=16,
    alignment=TA_JUSTIFY,
    spaceAfter=8,
    firstLineIndent=15,
)

body_noindent = ParagraphStyle(
    'VNBodyNoIndent',
    parent=body_style,
    firstLineIndent=0,
)

bullet_style = ParagraphStyle(
    'VNBullet',
    parent=body_style,
    fontSize=11,
    leading=15,
    leftIndent=20,
    bulletIndent=5,
    firstLineIndent=0,
    spaceAfter=4,
)

info_label = ParagraphStyle(
    'VNInfoLabel',
    parent=styles['Normal'],
    fontName='DejaVu-Bold',
    fontSize=11,
    leading=16,
)

caption_style = ParagraphStyle(
    'VNCaption',
    parent=styles['Normal'],
    fontName='DejaVu-Italic',
    fontSize=10,
    leading=13,
    alignment=TA_CENTER,
    spaceAfter=12,
    textColor=colors.HexColor('#4a5568'),
)

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def build_table(data, col_widths, header_bg='#2c5282', header_fg='#FFFFFF', body_bg='#f7fafc'):
    """Build a styled table for the thesis."""
    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(header_bg)),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor(header_fg)),
        ('FONTNAME', (0, 0), (-1, 0), 'DejaVu-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTNAME', (0, 1), (-1, -1), 'DejaVu'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor(body_bg)]),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    return t

def para_table_cell(text, style=None):
    """Wrap text in a paragraph for use in table cells."""
    if style is None:
        style = ParagraphStyle(
            'TableCell',
            fontName='DejaVu',
            fontSize=9,
            leading=12,
            alignment=TA_LEFT,
        )
    return Paragraph(text, style)

def bullet_list(items):
    """Create a bulleted list."""
    cell_style = ParagraphStyle(
        'BulletCell',
        fontName='DejaVu',
        fontSize=11,
        leading=15,
        alignment=TA_JUSTIFY,
    )
    flowables = []
    for item in items:
        flowables.append(ListItem(Paragraph(item, cell_style), leftIndent=15))
    return ListFlowable(flowables, bulletType='bullet', start='•', leftIndent=20)

# ============================================================
# BUILD DOCUMENT CONTENT
# ============================================================

output_path = '/home/claude/De_cuong_nghien_cuu_ITP.pdf'
doc = SimpleDocTemplate(
    output_path,
    pagesize=A4,
    leftMargin=2.5*cm,
    rightMargin=2*cm,
    topMargin=2.5*cm,
    bottomMargin=2*cm,
    title='Đề cương nghiên cứu — Dự đoán chảy máu ở bệnh nhân GTCMD',
    author='Trần Xuân Nhiên',
)

story = []

# ============================================================
# COVER PAGE
# ============================================================

story.append(Spacer(1, 0.5*cm))
story.append(Paragraph("ĐẠI HỌC Y DƯỢC THÀNH PHỐ HỒ CHÍ MINH", subtitle_style))
story.append(Paragraph("BỆNH VIỆN TRUYỀN MÁU HUYẾT HỌC", subtitle_style))
story.append(Spacer(1, 1.5*cm))

story.append(Paragraph("ĐỀ CƯƠNG NGHIÊN CỨU", title_style))
story.append(Paragraph("LUẬN VĂN CAO HỌC 2025–2027", subtitle_style))
story.append(Spacer(1, 1.2*cm))

thesis_title_style = ParagraphStyle(
    'ThesisTitle',
    parent=styles['Title'],
    fontName='DejaVu-Bold',
    fontSize=15,
    leading=22,
    alignment=TA_CENTER,
    textColor=colors.HexColor('#1a365d'),
)

story.append(Paragraph(
    "BƯỚC ĐẦU ĐÁNH GIÁ HIỆU QUẢ DỰ ĐOÁN CHẢY MÁU "
    "CỦA CÁC MÔ HÌNH HỌC MÁY KẾT HỢP HỆ THỐNG "
    "TRÍ TUỆ NHÂN TẠO TỰ ĐỘNG Ở BỆNH NHÂN "
    "NGƯỜI LỚN GIẢM TIỂU CẦU MIỄN DỊCH "
    "TẠI BỆNH VIỆN TRUYỀN MÁU HUYẾT HỌC "
    "GIAI ĐOẠN 2022–2026",
    thesis_title_style
))

story.append(Spacer(1, 1.5*cm))

info_table_data = [
    [Paragraph("<b>Học viên thực hiện:</b>", info_label),
     Paragraph("Trần Xuân Nhiên", body_noindent)],
    [Paragraph("<b>Khoá:</b>", info_label),
     Paragraph("Cao học 2025–2027", body_noindent)],
    [Paragraph("<b>Chuyên ngành:</b>", info_label),
     Paragraph("Huyết học — Truyền máu", body_noindent)],
    [Paragraph("<b>Đơn vị công tác:</b>", info_label),
     Paragraph("Khoa Huyết học Người lớn 2, Bệnh viện Truyền máu Huyết học TP.HCM", body_noindent)],
    [Paragraph("<b>Thời gian nghiên cứu:</b>", info_label),
     Paragraph("9 tháng (01/2025 – 09/2025)", body_noindent)],
]
info_table = Table(info_table_data, colWidths=[5*cm, 10*cm])
info_table.setStyle(TableStyle([
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
]))
story.append(info_table)

story.append(Spacer(1, 1.5*cm))
story.append(Paragraph("TP. Hồ Chí Minh, tháng 4 năm 2026", subtitle_style))

story.append(PageBreak())

# ============================================================
# 1. ĐẶT VẤN ĐỀ
# ============================================================

story.append(Paragraph("1. ĐẶT VẤN ĐỀ", heading1_style))

story.append(Paragraph(
    "Bệnh giảm tiểu cầu miễn dịch (GTCMD) nguyên phát là một rối loạn tự miễn dịch "
    "đặc trưng bởi tình trạng giảm tiểu cầu đơn độc, với số lượng tiểu cầu trong máu "
    "ngoại vi dưới 100 × 10<super>9</super>/L mà không có các nguyên nhân hoặc rối loạn khác có thể "
    "liên quan đến giảm tiểu cầu [1]. Vấn đề lâm sàng chính của GTCMD nguyên phát là "
    "tăng nguy cơ chảy máu, mặc dù các triệu chứng chảy máu không phải lúc nào cũng "
    "xuất hiện. Đây không chỉ là rối loạn huyết học đơn thuần mà còn gây áp lực tâm lý "
    "nặng nề do rủi ro xuất huyết khó dự báo, khiến bệnh nhân luôn bất an và lệ thuộc "
    "vào con số tiểu cầu [2, 3].",
    body_style
))

story.append(Paragraph(
    "Sự bất an này phản ánh một thực tế lâm sàng: dù Hiệp hội Huyết học Hoa Kỳ (ASH) "
    "năm 2019 đã có tiêu chuẩn nhập viện, nhưng tiêu chí xuất viện an toàn vẫn chưa "
    "được chuẩn hoá quốc tế [4, 5]. Hệ quả là việc ra quyết định hiện nay chủ yếu dựa "
    "trên kinh nghiệm lâm sàng (mức chứng cứ C), dẫn đến sự thiếu đồng nhất giữa các "
    "cơ sở y tế và lãng phí nguồn lực. Tại Việt Nam, các nghiên cứu vẫn tập trung vào "
    "đáp ứng điều trị hơn là xây dựng tiêu chí ra viện dựa trên dữ liệu thực tế [6, 7, 8].",
    body_style
))

story.append(Paragraph(
    "Thách thức cốt lõi của tình trạng trên nằm ở tính không đồng nhất của bệnh lý, "
    "nơi các ngưỡng cắt tiểu cầu truyền thống không phản ánh chính xác rủi ro thực tế "
    "do chịu tác động phức tạp từ tuổi, bệnh nền và thuốc phối hợp [9]. Hơn nữa, khả "
    "năng cầm máu thực tế phụ thuộc vào \"chất lượng\" (hoạt tính sinh học tiểu cầu) "
    "nhiều hơn là \"số lượng\" đơn thuần [10]. Nghiên cứu của Chen (2021) đã xác nhận "
    "tính chất phức tạp này khi chứng minh mối tương quan giữa số lượng tiểu cầu và "
    "rủi ro xuất huyết trở nên không tuyến tính, thậm chí mất hoàn toàn sự tương quan "
    "khi tiểu cầu trên mức 10 × 10<super>9</super>/L [11].",
    body_style
))

story.append(Paragraph(
    "Trong bối cảnh đó, học máy (Machine Learning) nổi lên như một giải pháp tối ưu "
    "nhờ khả năng phân tích các mối quan hệ phi tuyến tính đa biến để cá thể hoá dự "
    "báo rủi ro. Các mô hình như Random Forest, XGBoost, LightGBM và Logistic "
    "Regression đã chứng minh hiệu quả vượt trội với AUC đạt từ 0,82 đến 0,89 trong "
    "việc tiên lượng các biến cố xuất huyết nặng [5, 12]. An và cộng sự (2023) đã phát "
    "triển mô hình dự đoán chảy máu nghiêm trọng trên 3.191 bệnh nhân GTCMD người "
    "lớn tại Trung Quốc, với Random Forest đạt AUC 0,89 trong tập huấn luyện và 0,82 "
    "trong tập thử nghiệm tiến cứu [12].",
    body_style
))

story.append(Paragraph(
    "Song song với xu hướng học máy cổ điển, một hướng tiếp cận mới đang nổi lên là "
    "<b>Trí tuệ nhân tạo tự động đa tác tử (Agentic AI)</b>. Dhiman và cộng sự (2026) đã "
    "đề xuất khung Agentic AI cho chẩn đoán bệnh với các tác tử tự động phối hợp mà "
    "không cần can thiệp của người dùng, kết hợp mô hình ngôn ngữ lớn (LLM) với "
    "truy xuất thông tin tăng cường (RAG) để tạo ra giải thích dựa trên hướng dẫn y "
    "khoa chuẩn [13]. Cách tiếp cận này hứa hẹn khắc phục nhược điểm \"hộp đen\" "
    "của các mô hình học máy truyền thống, tăng độ tin cậy của bác sĩ vào hệ thống hỗ "
    "trợ quyết định.",
    body_style
))

story.append(Paragraph(
    "Tuy nhiên, trái ngược với xu hướng quốc tế, tại Việt Nam việc ứng dụng cả hai "
    "công nghệ này trong quản lý bệnh nhân GTCMD vẫn chưa được tiếp cận một cách "
    "có hệ thống, tạo nên một khoảng trống nghiên cứu đáng kể trong việc tối ưu hoá "
    "quy trình ra quyết định lâm sàng.",
    body_style
))

story.append(Paragraph(
    "Vì những lý do trên, chúng tôi thực hiện đề tài: <i>\"Bước đầu đánh giá hiệu quả "
    "dự đoán chảy máu của các mô hình học máy kết hợp hệ thống trí tuệ nhân tạo tự "
    "động ở bệnh nhân người lớn giảm tiểu cầu miễn dịch tại Bệnh viện Truyền máu "
    "Huyết học giai đoạn 2022–2026\"</i>. Nghiên cứu nhằm xây dựng cơ sở khoa học "
    "khách quan để cá thể hoá đánh giá rủi ro và hỗ trợ quyết định xuất viện an toàn, "
    "đồng thời ứng dụng công nghệ tiên tiến để cung cấp giải thích lâm sàng minh bạch "
    "cho bác sĩ, góp phần làm giảm gánh nặng bệnh tật cũng như cải thiện chất lượng "
    "cuộc sống cho người bệnh.",
    body_style
))

# ============================================================
# 2. MỤC TIÊU NGHIÊN CỨU
# ============================================================

story.append(Paragraph("2. MỤC TIÊU NGHIÊN CỨU", heading1_style))

story.append(Paragraph("2.1. Mục tiêu tổng quát", heading2_style))
story.append(Paragraph(
    "Xây dựng và đánh giá hệ thống hỗ trợ quyết định lâm sàng dựa trên học máy và trí "
    "tuệ nhân tạo tự động nhằm dự đoán nguy cơ chảy máu ở bệnh nhân người lớn "
    "GTCMD tại Bệnh viện Truyền máu Huyết học TP.HCM.",
    body_style
))

story.append(Paragraph("2.2. Mục tiêu cụ thể", heading2_style))

objectives = [
    "<b>Mục tiêu 1:</b> Mô tả đặc điểm lâm sàng, cận lâm sàng và thực trạng xuất "
    "huyết của bệnh nhân GTCMD người lớn tại Bệnh viện Truyền máu Huyết học (BV "
    "TMHH) giai đoạn 2022–2026.",
    "<b>Mục tiêu 2:</b> Xác định và so sánh hiệu suất dự báo (AUC, độ nhạy, độ đặc "
    "hiệu, độ chính xác) của các mô hình học máy: Random Forest, XGBoost, "
    "LightGBM và Logistic Regression; đồng thời xác định tầm quan trọng của các "
    "yếu tố tiên lượng thông qua phân tích SHAP.",
    "<b>Mục tiêu 3:</b> Xây dựng một ứng dụng trực tuyến tích hợp hệ thống trí tuệ "
    "nhân tạo tự động (Agentic AI) để hỗ trợ các bác sĩ lâm sàng nhận diện nhanh "
    "nguy cơ xuất huyết và nhận giải thích lâm sàng dựa trên hướng dẫn y khoa "
    "chuẩn.",
]
story.append(bullet_list(objectives))

# ============================================================
# 3. ĐỐI TƯỢNG VÀ PHƯƠNG PHÁP NGHIÊN CỨU
# ============================================================

story.append(Paragraph("3. ĐỐI TƯỢNG VÀ PHƯƠNG PHÁP NGHIÊN CỨU", heading1_style))

story.append(Paragraph("3.1. Đối tượng nghiên cứu", heading2_style))

story.append(Paragraph("<b>Tiêu chuẩn lựa chọn:</b>", heading3_style))
story.append(bullet_list([
    "Bệnh nhân người lớn (≥ 18 tuổi) được chẩn đoán GTCMD nguyên phát tại BV TMHH trong giai đoạn nghiên cứu.",
    "Thoả mãn các tiêu chuẩn chẩn đoán GTCMD theo ASH 2019 [4].",
]))

story.append(Paragraph("<b>Tiêu chuẩn loại trừ:</b>", heading3_style))
story.append(bullet_list([
    "Bệnh nhân mắc các bệnh lý gây giảm tiểu cầu thứ phát (Lupus, ung thư di căn tuỷ, suy tuỷ...).",
    "Bệnh nhân có bệnh án không đầy đủ thông tin về các biến số nghiên cứu.",
    "Bệnh nhân đang trong tình trạng xuất huyết nghiêm trọng tại thời điểm đánh giá.",
]))

story.append(Paragraph("<b>Cỡ mẫu:</b>", heading3_style))
story.append(Paragraph(
    "Cỡ mẫu toàn bộ các trường hợp thoả tiêu chuẩn trong giai đoạn nghiên cứu "
    "(dự kiến tối thiểu đạt ngưỡng ý nghĩa thống kê theo công thức tính cỡ mẫu "
    "n = 150 bệnh nhân).",
    body_style
))

story.append(Paragraph("<b>Địa điểm và thời gian:</b>", heading3_style))
story.append(bullet_list([
    "<b>Địa điểm:</b> Khoa Huyết học Người lớn 2, Bệnh viện Truyền máu Huyết học TP.HCM.",
    "<b>Thời gian thu thập dữ liệu:</b> Từ tháng 01/2022 đến tháng 05/2026.",
    "<b>Thời gian thực hiện nghiên cứu:</b> 9 tháng (01/2025 – 09/2025).",
]))

story.append(Paragraph("3.2. Thiết kế nghiên cứu", heading2_style))
story.append(Paragraph(
    "Nghiên cứu hồi cứu, mô tả hàng loạt ca, kết hợp phát triển và kiểm định mô hình dự báo.",
    body_style
))

story.append(Paragraph("3.3. Danh mục các biến số chính", heading2_style))

variables_data = [
    ['STT', 'Tên biến số', 'Loại biến', 'Giá trị / Đơn vị'],
    ['1', para_table_cell('Nhiễm trùng'), 'Định tính', 'Có / Không'],
    ['2', para_table_cell('Đái tháo đường chưa kiểm soát'), 'Định tính', 'Có / Không'],
    ['3', para_table_cell('Tuổi'), 'Định lượng', 'Năm (Trung vị, Q1-Q3)'],
    ['4', para_table_cell('Phân loại GTCMD'), 'Định tính',
     para_table_cell('Mới chẩn đoán / Dai dẳng / Mạn tính')],
    ['5', para_table_cell('Bệnh lý tim mạch (CVD)'), 'Định tính', 'Có / Không'],
    ['6', para_table_cell('Số lượng Lymphocyte thấp'), 'Định tính',
     para_table_cell('< 1 × 10<super>9</super>/L')],
    ['7', para_table_cell('Xuất huyết da và niêm mạc'), 'Định tính', 'Có / Không'],
    ['8', para_table_cell('Số lượng tiểu cầu ban đầu'), 'Định lượng',
     para_table_cell('× 10<super>9</super>/L')],
    ['9', para_table_cell('Số lượng tiểu cầu thấp hiện tại'), 'Định tính',
     para_table_cell('< 20 × 10<super>9</super>/L')],
    ['10', para_table_cell('Thời gian mắc bệnh'), 'Định lượng', 'Tháng / Năm'],
]

story.append(build_table(
    variables_data,
    col_widths=[1*cm, 6*cm, 3*cm, 5.5*cm],
))

story.append(Paragraph(
    "<b>Biến cố đầu ra (Outcome):</b> Tình trạng xuất huyết từ độ 2 trở lên theo thang "
    "điểm WHO trên lâm sàng.",
    body_style
))

# ============================================================
# 4. PHƯƠNG PHÁP KỸ THUẬT
# ============================================================

story.append(Paragraph("4. PHƯƠNG PHÁP KỸ THUẬT VÀ KIẾN TRÚC HỆ THỐNG", heading1_style))

story.append(Paragraph("4.1. Cách tiếp cận tổng thể", heading2_style))
story.append(Paragraph(
    "Nghiên cứu áp dụng cách tiếp cận lai (hybrid), kết hợp học máy cổ điển với hệ "
    "thống trí tuệ nhân tạo tự động đa tác tử (Agentic AI). Mô hình học máy đóng vai "
    "trò lõi dự đoán, trong khi lớp Agentic AI bao phủ bên ngoài để cung cấp giao tiếp "
    "bằng ngôn ngữ tự nhiên và giải thích lâm sàng dựa trên hướng dẫn y khoa chuẩn. "
    "Cách tiếp cận này vừa đảm bảo tính khoa học, khả thi cho luận văn y khoa, vừa "
    "tạo ra đóng góp kỹ thuật mới mẻ cho lĩnh vực.",
    body_style
))

story.append(Paragraph("4.2. Quy trình xây dựng mô hình học máy", heading2_style))
story.append(bullet_list([
    "<b>Cân bằng dữ liệu:</b> Sử dụng kỹ thuật SMOTE (Synthetic Minority Over-sampling Technique) để cân bằng giữa nhóm có và không có biến cố xuất huyết.",
    "<b>Chia tập dữ liệu:</b> Tỉ lệ 80% huấn luyện (Training) và 20% kiểm tra (Test).",
    "<b>Tối ưu hoá tham số:</b> Áp dụng GridSearchCV và tối ưu hoá Bayesian thông qua SageMaker Automatic Model Tuning.",
    "<b>Phân tích tầm quan trọng:</b> Sử dụng SHAP (Shapley Additive Explanations) thông qua SageMaker Clarify để giải thích mô hình.",
    "<b>Đánh giá mô hình:</b> Dựa trên AUC, độ nhạy, độ đặc hiệu, độ chính xác và đường cong hiệu chuẩn (calibration curves).",
    "<b>Kiểm định chéo:</b> Áp dụng cross-validation 10-fold phân tầng (stratified) để đánh giá độ ổn định của mô hình.",
]))

story.append(Paragraph("4.3. Kiến trúc hệ thống trên Nền tảng Đám mây AWS", heading2_style))
story.append(Paragraph(
    "Hệ thống được triển khai trên Amazon Web Services (AWS) với kiến trúc bốn lớp, "
    "tuân theo khuyến nghị của AWS Healthcare Industry Lens [14] và các hệ thống "
    "tham chiếu quốc tế như ALMA (Catalonia) và NoHarm (Brazil).",
    body_style
))

story.append(Paragraph("<b>Lớp 1 — Thu thập và lưu trữ dữ liệu:</b>", heading3_style))
story.append(bullet_list([
    "<b>Amazon S3:</b> Lưu trữ hồ sơ bệnh án điện tử được mã hoá và phi định danh.",
    "<b>AWS Glue:</b> Quy trình ETL tự động (làm sạch, mã hoá biến phân loại, xử lý giá trị khuyết).",
    "<b>Amazon DynamoDB / S3 Feature Store:</b> Lưu trữ vector đặc trưng bệnh nhân để truy xuất nhanh.",
    "<b>Amazon Aurora Serverless v2 (pgvector):</b> Lưu trữ vector embedding của các hướng dẫn lâm sàng (ASH, ISTH, phác đồ BV TMHH).",
]))

story.append(Paragraph("<b>Lớp 2 — Huấn luyện và triển khai mô hình học máy:</b>", heading3_style))
story.append(bullet_list([
    "<b>Amazon SageMaker:</b> Huấn luyện 4 mô hình học máy (Random Forest, XGBoost, LightGBM, Logistic Regression).",
    "<b>SageMaker Serverless Inference:</b> Triển khai mô hình tốt nhất với chi phí thấp, tự động mở rộng theo yêu cầu.",
    "<b>SageMaker Clarify:</b> Tạo giá trị SHAP và phát hiện thiên lệch (bias) trong mô hình.",
]))

story.append(Paragraph("<b>Lớp 3 — Điều phối Agentic AI:</b>", heading3_style))
story.append(bullet_list([
    "<b>Tác tử Trợ lý Bác sĩ Thông minh (IDA):</b> Tác tử giám sát, phân phối truy vấn đến các tác tử con.",
    "<b>Tác tử Xử lý Dữ liệu (Data Processing Agent):</b> Lambda function kiểm tra và chuẩn hoá đầu vào.",
    "<b>Tác tử Dự đoán (Prediction Agent):</b> Gọi SageMaker endpoint và trả về xác suất chảy máu.",
    "<b>Tác tử Giải thích (Explanation Agent):</b> Sử dụng RAG và LLM (Claude Haiku / Nova Micro) để tạo giải thích lâm sàng bằng tiếng Việt dựa trên hướng dẫn ASH/ISTH.",
    "<b>Amazon Bedrock Guardrails:</b> Lọc nội dung, bảo vệ thông tin bệnh nhân (PHI).",
]))

story.append(Paragraph("<b>Lớp 4 — Ứng dụng và phân phối:</b>", heading3_style))
story.append(bullet_list([
    "<b>Amazon API Gateway + Cognito:</b> API xác thực bảo mật cho bác sĩ BV TMHH.",
    "<b>Ứng dụng web React:</b> Giao diện tiếng Việt, hiển thị điểm nguy cơ, biểu đồ SHAP waterfall, và giải thích lâm sàng.",
    "<b>Amazon CloudFront:</b> Phân phối nội dung nhanh tại Việt Nam.",
    "<b>Amazon CloudWatch:</b> Giám sát, ghi log và vết kiểm toán.",
]))

story.append(Paragraph("4.4. Phần mềm và công cụ phân tích thống kê", heading2_style))
story.append(bullet_list([
    "<b>Phân tích học máy:</b> Python với các thư viện Scikit-learn, XGBoost, LightGBM, Pandas, NumPy.",
    "<b>Phân tích thống kê:</b> STATA 17.0.",
    "<b>Giải thích mô hình:</b> SHAP library + Amazon SageMaker Clarify.",
    "<b>Kiểm định thống kê:</b> Chi-square, Fisher, Mann-Whitney U hoặc t-test tuỳ theo phân phối của dữ liệu.",
]))

story.append(PageBreak())

# ============================================================
# 5. KẾ HOẠCH THỰC HIỆN
# ============================================================

story.append(Paragraph("5. KẾ HOẠCH THỰC HIỆN (9 THÁNG)", heading1_style))

story.append(Paragraph("5.1. Giai đoạn 1: Nền tảng và Kỹ thuật Dữ liệu (Tháng 1–2)", heading2_style))
phase1_data = [
    ['Tuần', 'Công việc', 'Sản phẩm'],
    ['1–2', para_table_cell('Thiết lập tài khoản AWS, IAM, VPC, rà soát tuân thủ HIPAA'),
     para_table_cell('Môi trường đám mây an toàn')],
    ['3–4', para_table_cell('Xây dựng cấu trúc S3 data lake; phát triển quy trình ETL AWS Glue'),
     para_table_cell('Hệ thống thu thập dữ liệu tự động')],
    ['5–6', para_table_cell('Làm sạch dữ liệu, xử lý giá trị khuyết, phân tích thăm dò (EDA)'),
     para_table_cell('Bộ dữ liệu sạch + báo cáo EDA')],
    ['7–8', para_table_cell('Kỹ thuật đặc trưng, SMOTE oversampling, chia tập huấn luyện/kiểm tra'),
     para_table_cell('Kho đặc trưng (Feature Store)')],
]
story.append(build_table(phase1_data, col_widths=[1.5*cm, 9*cm, 5*cm]))
story.append(Paragraph(
    "<b>Đầu ra cho luận văn:</b> Mục tiêu 1 — Mô tả đặc điểm lâm sàng, cận lâm sàng và thực trạng xuất huyết.",
    caption_style
))

story.append(Paragraph("5.2. Giai đoạn 2: Phát triển và Đánh giá Mô hình Học máy (Tháng 3–4)", heading2_style))
phase2_data = [
    ['Tuần', 'Công việc', 'Sản phẩm'],
    ['9–10', para_table_cell('Huấn luyện 4 mô hình học máy (RF, XGBoost, LightGBM, LR) trên SageMaker Studio'),
     para_table_cell('Các mô hình đã huấn luyện')],
    ['11–12', para_table_cell('Tối ưu hoá siêu tham số qua GridSearchCV / Bayesian optimization'),
     para_table_cell('Mô hình tối ưu')],
    ['13–14', para_table_cell('Đánh giá mô hình: AUC, độ nhạy, độ đặc hiệu, độ chính xác, đường cong hiệu chuẩn'),
     para_table_cell('Báo cáo so sánh hiệu suất')],
    ['15–16', para_table_cell('Phân tích SHAP với SageMaker Clarify; xếp hạng tầm quan trọng đặc trưng'),
     para_table_cell('Báo cáo khả năng giải thích')],
]
story.append(build_table(phase2_data, col_widths=[1.5*cm, 9*cm, 5*cm]))
story.append(Paragraph(
    "<b>Đầu ra cho luận văn:</b> Mục tiêu 2 — So sánh mô hình và phân tích tầm quan trọng yếu tố tiên lượng.",
    caption_style
))

story.append(Paragraph("5.3. Giai đoạn 3: Xây dựng Lớp Agentic AI (Tháng 5–6)", heading2_style))
phase3_data = [
    ['Tuần', 'Công việc', 'Sản phẩm'],
    ['17–18', para_table_cell('Triển khai mô hình ML tốt nhất lên SageMaker endpoint; xây dựng Lambda functions'),
     para_table_cell('API dự đoán thời gian thực')],
    ['19–20', para_table_cell('Nhúng hướng dẫn lâm sàng (ASH, ISTH, phác đồ Việt Nam) vào vector store'),
     para_table_cell('Cơ sở tri thức RAG')],
    ['21–22', para_table_cell('Xây dựng Bedrock Agents: IDA giám sát, xử lý dữ liệu, dự đoán, giải thích'),
     para_table_cell('Pipeline agent hoạt động')],
    ['23–24', para_table_cell('Cấu hình Bedrock Guardrails; triển khai prompt caching; kiểm thử điều phối agent'),
     para_table_cell('Hệ thống agent an toàn, tối ưu')],
]
story.append(build_table(phase3_data, col_widths=[1.5*cm, 9*cm, 5*cm]))

story.append(Paragraph("5.4. Giai đoạn 4: Phát triển Ứng dụng (Tháng 7)", heading2_style))
phase4_data = [
    ['Tuần', 'Công việc', 'Sản phẩm'],
    ['25–26', para_table_cell('Xây dựng ứng dụng web React với giao diện tiếng Việt; tích hợp API Gateway + Cognito'),
     para_table_cell('Ứng dụng frontend')],
    ['27–28', para_table_cell('Xây dựng dashboard: gauge nguy cơ, biểu đồ SHAP waterfall, panel giải thích, lịch sử bệnh nhân'),
     para_table_cell('Giao diện lâm sàng hoàn chỉnh')],
]
story.append(build_table(phase4_data, col_widths=[1.5*cm, 9*cm, 5*cm]))
story.append(Paragraph(
    "<b>Đầu ra cho luận văn:</b> Mục tiêu 3 — Công cụ lâm sàng trực tuyến.",
    caption_style
))

story.append(Paragraph("5.5. Giai đoạn 5: Kiểm thử, Đánh giá và Tối ưu hoá (Tháng 8–9)", heading2_style))
phase5_data = [
    ['Tuần', 'Công việc', 'Sản phẩm'],
    ['29–30', para_table_cell('Kiểm thử nội bộ: unit test, integration test, load test'),
     para_table_cell('Báo cáo kiểm thử')],
    ['31–32', para_table_cell('Kiểm thử chấp nhận người dùng (UAT) với 5–10 bác sĩ tại BV TMHH'),
     para_table_cell('Phản hồi từ UAT')],
    ['33–34', para_table_cell('A/B testing giữa các mô hình; đánh giá RAG bằng LLM-as-a-judge'),
     para_table_cell('Xác nhận lựa chọn mô hình')],
    ['35–36', para_table_cell('Tối ưu chi phí, tài liệu hoá, triển khai cuối, hỗ trợ viết luận văn'),
     para_table_cell('Hệ thống production + luận văn')],
]
story.append(build_table(phase5_data, col_widths=[1.5*cm, 9*cm, 5*cm]))

story.append(PageBreak())

# ============================================================
# 6. CẢI TIẾN KỸ THUẬT
# ============================================================

story.append(Paragraph("6. CÁC CẢI TIẾN KỸ THUẬT ĐƯỢC KÍCH HOẠT BỞI KHUNG THỜI GIAN 9 THÁNG", heading1_style))

story.append(Paragraph("6.1. Cải tiến Mô hình Học máy", heading2_style))
story.append(bullet_list([
    "<b>Tối ưu hoá Siêu tham số Bayesian:</b> Thay thế GridSearchCV bằng SageMaker Automatic Model Tuning để tìm kiếm tham số hiệu quả hơn trên cả 4 mô hình.",
    "<b>Ensemble Stacking:</b> Xây dựng mô hình meta kết hợp RF, XGBoost, LightGBM, LR để đạt AUC cao hơn mô hình đơn.",
    "<b>Đường cong hiệu chuẩn (Calibration Curves):</b> Thêm Platt scaling hoặc isotonic regression để đảm bảo xác suất dự đoán được hiệu chuẩn tốt — rất quan trọng cho điểm nguy cơ lâm sàng.",
    "<b>Chiến lược kiểm định chéo:</b> Sử dụng stratified 10-fold CV thay vì chia train/test đơn giản.",
    "<b>Giám sát Mô hình:</b> SageMaker Model Monitor phát hiện trôi dữ liệu và suy giảm mô hình theo thời gian.",
]))

story.append(Paragraph("6.2. Cải tiến Agentic AI", heading2_style))
story.append(bullet_list([
    "<b>Đàm thoại đa lượt:</b> Cho phép tác tử IDA xử lý câu hỏi tiếp theo (ví dụ \"Nếu bệnh nhân còn bị nhiễm trùng thì sao?\") thông qua quản lý phiên Bedrock.",
    "<b>Đánh giá LLM-as-a-Judge:</b> Dùng một LLM khác để đánh giá chất lượng, độ chính xác và tính liên quan lâm sàng của đầu ra — phương pháp AWS đã trình diễn cho RAG y tế [15].",
    "<b>Prompt Caching:</b> Lưu cache system prompt và ngữ cảnh hướng dẫn lâm sàng để giảm độ trễ và chi phí tới 90% trên các truy vấn lặp lại.",
    "<b>Intelligent Prompt Routing:</b> Dùng tính năng routing của Bedrock để gửi truy vấn đơn giản đến mô hình rẻ hơn (Nova Micro/Haiku) và truy vấn phức tạp đến mô hình mạnh hơn.",
    "<b>Self-Correcting RAG:</b> Triển khai vòng lặp truy xuất-đánh giá-tinh chỉnh trong tác tử giải thích.",
]))

story.append(Paragraph("6.3. Cải tiến Ứng dụng", heading2_style))
story.append(bullet_list([
    "<b>Cơ chế phản hồi:</b> Cho phép bác sĩ đánh giá chất lượng dự đoán (👍/👎), lưu phản hồi vào DynamoDB để huấn luyện lại mô hình trong tương lai.",
    "<b>Chế độ offline:</b> Cache các phản hồi hướng dẫn thường dùng tại chỗ để ứng dụng hoạt động với kết nối internet không ổn định (phổ biến ở môi trường bệnh viện Việt Nam).",
    "<b>Giao diện đáp ứng thiết bị di động:</b> Tối ưu cho sử dụng trên máy tính bảng tại giường bệnh.",
]))

# ============================================================
# 7. DỰ TOÁN KINH PHÍ
# ============================================================

story.append(Paragraph("7. DỰ TOÁN KINH PHÍ HẠ TẦNG ĐÁM MÂY", heading1_style))

story.append(Paragraph(
    "Nghiên cứu đề xuất hai phương án triển khai trên nền tảng AWS, phù hợp với các "
    "mức độ đầu tư và yêu cầu khác nhau.",
    body_style
))

story.append(Paragraph("7.1. Phương án A: Triển khai đầy đủ tiềm năng", heading2_style))
story.append(Paragraph(
    "Phương án cung cấp khả năng tối đa với hiệu suất cao nhất, đầy đủ tính năng và "
    "hạ tầng cấp sản xuất. Bao gồm 20 dịch vụ AWS.",
    body_style
))

option_a_cost = [
    ['Hạng mục', 'Chi phí / tháng', 'Ghi chú'],
    [para_table_cell('SageMaker (Studio, Training, Endpoint, Clarify, Feature Store, Monitor)'),
     '$205–330', 'Endpoint luôn hoạt động'],
    [para_table_cell('Amazon Bedrock (Claude Sonnet + Agents + KB + Guardrails)'),
     '$100–195', 'LLM chất lượng cao'],
    [para_table_cell('Amazon OpenSearch Serverless (vector store RAG)'),
     '$350–400', 'Sàn tối thiểu ~$350/tháng'],
    [para_table_cell('Dịch vụ dữ liệu (S3, Glue, DynamoDB)'),
     '$20–40', 'Pipeline và lưu trữ'],
    [para_table_cell('Dịch vụ ứng dụng (Lambda, API GW, Cognito, CloudFront, Amplify)'),
     '$17–40', 'Frontend + backend'],
    [para_table_cell('Giám sát và dashboard (CloudWatch + QuickSight)'),
     '$34–44', 'Phân tích nâng cao'],
    [para_table_cell('<b>TỔNG MỖI THÁNG</b>'),
     para_table_cell('<b>$720–1,040</b>'), ''],
    [para_table_cell('<b>TỔNG 9 THÁNG</b>'),
     para_table_cell('<b>$6,500–9,400</b>'),
     para_table_cell('≈ 165–238 triệu VNĐ')],
]
story.append(build_table(option_a_cost, col_widths=[7*cm, 3.5*cm, 5*cm]))

story.append(Paragraph("7.2. Phương án B: Tối ưu chi phí", heading2_style))
story.append(Paragraph(
    "Phương án đạt được các mục tiêu nghiên cứu cốt lõi với chi phí giảm đáng kể. "
    "Đánh đổi một số tính năng production-grade để có khả năng chi trả. Bao gồm 14 "
    "dịch vụ AWS.",
    body_style
))

option_b_cost = [
    ['Hạng mục', 'Chi phí / tháng', 'Ghi chú'],
    [para_table_cell('SageMaker Training + Serverless Inference'),
     '$15–35', 'Spot instances, pay-per-request'],
    [para_table_cell('Amazon Bedrock (Nova Micro + Haiku + Agents + KB)'),
     '$15–35', 'LLM rẻ + prompt caching'],
    [para_table_cell('Aurora Serverless v2 (pgvector) — thay thế OpenSearch'),
     '$15–30', '<b>Tiết kiệm ~$335/tháng</b>'],
    [para_table_cell('Dịch vụ dữ liệu (S3, Glue, DynamoDB)'),
     '$10–20', 'Pipeline tối giản'],
    [para_table_cell('Dịch vụ ứng dụng (Lambda, API GW, Cognito, CloudFront)'),
     '$5–15', 'Chủ yếu trong free tier'],
    [para_table_cell('CloudWatch cơ bản'),
     '$5–10', 'Các metric thiết yếu'],
    [para_table_cell('<b>TỔNG MỖI THÁNG</b>'),
     para_table_cell('<b>$65–155</b>'), ''],
    [para_table_cell('<b>TỔNG 9 THÁNG</b>'),
     para_table_cell('<b>$585–1,395</b>'),
     para_table_cell('≈ 15–36 triệu VNĐ')],
]
story.append(build_table(option_b_cost, col_widths=[7*cm, 3.5*cm, 5*cm]))

story.append(Paragraph("7.3. So sánh và khuyến nghị", heading2_style))

compare_data = [
    ['Tiêu chí', 'Phương án A — Đầy đủ', 'Phương án B — Tối ưu'],
    [para_table_cell('Chi phí / tháng'), '$720–1,040', '$65–155'],
    [para_table_cell('Tổng 9 tháng'), '$6,500–9,400', '$585–1,395'],
    [para_table_cell('Số dịch vụ AWS'), '20', '14'],
    [para_table_cell('Mô hình LLM'),
     para_table_cell('Claude Sonnet (chất lượng cao)'),
     para_table_cell('Nova Micro / Haiku (tốt)')],
    [para_table_cell('Vector store'),
     para_table_cell('OpenSearch Serverless'),
     para_table_cell('Aurora pgvector')],
    [para_table_cell('ML inference'),
     para_table_cell('Endpoint luôn hoạt động'),
     para_table_cell('Serverless (pay-per-request)')],
    [para_table_cell('Phù hợp với'),
     para_table_cell('Sẵn sàng xuất bản, cấp sản xuất'),
     para_table_cell('Dự án nghiên cứu, trình diễn luận văn')],
]
story.append(build_table(compare_data, col_widths=[4*cm, 5.5*cm, 6*cm]))

story.append(Paragraph("<b>Khuyến nghị:</b>", heading3_style))
story.append(Paragraph(
    "<b>Bắt đầu với Phương án B</b> trong Tháng 1–7 (giai đoạn phát triển và kiểm thử "
    "ban đầu), sau đó <b>nâng cấp chọn lọc các thành phần của Phương án A</b> trong "
    "Tháng 8–9 nếu ngân sách cho phép và các tính năng cụ thể cần thiết. Lộ trình "
    "nâng cấp:",
    body_style
))
story.append(bullet_list([
    "<b>Nâng cấp 1:</b> Aurora pgvector → OpenSearch Serverless (chỉ khi chất lượng RAG không đủ).",
    "<b>Nâng cấp 2:</b> Claude Haiku → Claude Sonnet (chỉ khi chất lượng giải thích cần cải thiện).",
    "<b>Nâng cấp 3:</b> Serverless Inference → Endpoint luôn hoạt động (chỉ khi độ trễ là vấn đề trong UAT).",
]))

story.append(Paragraph(
    "Cách tiếp cận theo giai đoạn này giữ tổng chi phí 9 tháng ở mức khoảng "
    "<b>$800–2,500 (tương đương 20–64 triệu VNĐ)</b> trong khi vẫn duy trì tính linh "
    "hoạt để mở rộng quy mô ở những điểm quan trọng.",
    body_style
))

story.append(Paragraph("7.4. Các mẹo tối ưu chi phí", heading2_style))
story.append(bullet_list([
    "<b>AWS Activate for Startups/Research:</b> Đăng ký credit AWS (lên đến $5,000–$100,000) — các dự án học thuật/nghiên cứu thường đủ điều kiện.",
    "<b>AWS Free Tier:</b> Lambda (1M requests), DynamoDB (25GB), S3 (5GB), Cognito (50K MAU), CloudWatch (cơ bản) đều miễn phí.",
    "<b>Spot Instances:</b> Sử dụng cho SageMaker training — tiết kiệm 60–90% so với on-demand.",
    "<b>Bedrock Flex Tier:</b> Giảm 50% cho inference không khẩn cấp.",
    "<b>AWS Budgets:</b> Đặt giới hạn chi tiêu hàng tháng và cảnh báo ở các ngưỡng 50%, 80%, 100%.",
    "<b>Tắt tài nguyên không dùng:</b> Xoá các SageMaker endpoint và notebook instance khi không sử dụng.",
]))

story.append(PageBreak())

# ============================================================
# 8. PHÂN TÍCH RỦI RO
# ============================================================

story.append(Paragraph("8. PHÂN TÍCH RỦI RO VÀ BIỆN PHÁP GIẢM THIỂU", heading1_style))

risk_data = [
    ['Rủi ro', 'Ảnh hưởng', 'Biện pháp giảm thiểu'],
    [para_table_cell('Chi phí OpenSearch Serverless tối thiểu ($350/tháng)'),
     para_table_cell('Vượt ngân sách'),
     para_table_cell('Sử dụng Aurora pgvector (Phương án B)')],
    [para_table_cell('Nhân token của Bedrock agent (5–10x)'),
     para_table_cell('Chi phí LLM bất ngờ'),
     para_table_cell('Đặt giới hạn MaxTokens; sử dụng prompt caching')],
    [para_table_cell('SageMaker endpoint chạy 24/7 không sử dụng'),
     para_table_cell('Lãng phí $80–120/tháng'),
     para_table_cell('Dùng Serverless Inference hoặc lịch tự tắt')],
    [para_table_cell('Khối lượng log CloudWatch'),
     para_table_cell('$0,50/GB ingestion tích luỹ'),
     para_table_cell('Đặt retention log 7 ngày; lọc log dài dòng')],
    [para_table_cell('LLM ảo giác trong ngữ cảnh lâm sàng'),
     para_table_cell('An toàn bệnh nhân'),
     para_table_cell('Bedrock Guardrails + template đầu ra có cấu trúc')],
    [para_table_cell('Tập dữ liệu nhỏ (n~150) quá khớp (overfitting)'),
     para_table_cell('Khái quát hoá kém'),
     para_table_cell('Cross-validation, regularization, ensemble')],
    [para_table_cell('Chất lượng dữ liệu từ EHR bệnh viện'),
     para_table_cell('Đặc trưng nhiễu'),
     para_table_cell('EDA chi tiết trong Giai đoạn 1; xác nhận lâm sàng')],
]
story.append(build_table(risk_data, col_widths=[5.5*cm, 3.5*cm, 6.5*cm]))

# ============================================================
# 9. Ý NGHĨA KHOA HỌC VÀ THỰC TIỄN
# ============================================================

story.append(Paragraph("9. Ý NGHĨA KHOA HỌC VÀ THỰC TIỄN", heading1_style))

story.append(Paragraph("9.1. Ý nghĩa khoa học", heading2_style))
story.append(bullet_list([
    "Đây là nghiên cứu đầu tiên tại Việt Nam xây dựng mô hình dự đoán chảy máu bằng học máy cho bệnh nhân GTCMD người lớn.",
    "Đóng góp mới trong việc tích hợp học máy cổ điển với hệ thống Agentic AI cho chẩn đoán và tiên lượng bệnh huyết học.",
    "Cung cấp bằng chứng về tính khả thi của việc triển khai các hệ thống AI y khoa hiện đại trên hạ tầng đám mây trong bối cảnh y tế Việt Nam.",
]))

story.append(Paragraph("9.2. Ý nghĩa thực tiễn", heading2_style))
story.append(bullet_list([
    "Cung cấp công cụ lâm sàng thực tế hỗ trợ bác sĩ tại BV TMHH trong việc ra quyết định nhanh chóng và chính xác.",
    "Cá thể hoá đánh giá rủi ro xuất huyết, giảm tình trạng thiếu đồng nhất trong ra quyết định lâm sàng.",
    "Hỗ trợ quyết định xuất viện an toàn, tối ưu hoá nguồn lực y tế và giảm thời gian nằm viện không cần thiết.",
    "Giao diện tiếng Việt giúp bác sĩ dễ dàng sử dụng mà không cần đào tạo chuyên sâu về công nghệ.",
    "Kiến trúc có khả năng mở rộng cho các bệnh lý huyết học khác trong tương lai.",
]))

# ============================================================
# 10. TÀI LIỆU THAM KHẢO
# ============================================================

story.append(Paragraph("10. TÀI LIỆU THAM KHẢO", heading1_style))

ref_style = ParagraphStyle(
    'Ref',
    parent=body_style,
    fontSize=10,
    leading=13,
    firstLineIndent=0,
    leftIndent=20,
    bulletIndent=0,
    spaceAfter=6,
)

references = [
    "Rodeghiero F, Stasi R, Gernsheimer T, et al. Standardization of terminology, definitions and outcome criteria in immune thrombocytopenic purpura of adults and children: report from an international working group. <i>Blood</i>. 2009;113(11):2386-93.",
    "Cooper N, Kruse A, Kruse C. A patient's perspective on impact of immune thrombocytopenia and emotional wellbeing: ITP World Impact Survey (I-WISh). 2020;EP1654(294135).",
    "Kruse C, Kruse A, DiRaimo J, et al. Immune thrombocytopenia: the patient's perspective. <i>Annals of Blood</i>. 2020;6.",
    "Neunert C, Terrell DR, Arnold DM, et al. American Society of Hematology 2019 guidelines for immune thrombocytopenia. <i>Blood Advances</i>. 2019;3(23):3829-66.",
    "Shen X, Guo X, Liu Y, et al. Prediction of moderate to severe bleeding risk in pediatric immune thrombocytopenia using machine learning. <i>European Journal of Pediatrics</i>. 2025;184(5):283.",
    "Nhi TT. Xác định giá trị IPF (Immature Platelet Fraction) trong chẩn đoán và đánh giá đáp ứng điều trị Corticosteroid ở bệnh nhân giảm tiểu cầu miễn dịch nguyên phát mới chẩn đoán. <i>Luận văn Thạc sĩ Y học</i>, Đại học Y Dược TP.HCM. 2022.",
    "Tuyền HTT. Đánh giá hiệu quả của Eltrombopag trong điều trị xuất huyết giảm tiểu cầu miễn dịch dai dẳng và mạn tính tại Bệnh viện Truyền máu - Huyết học. <i>Luận văn Chuyên khoa cấp II</i>, Đại học Y Dược TP.HCM. 2024.",
    "Hà Văn Quang, Đào HT. Đặc điểm lâm sàng và cận lâm sàng của bệnh nhân giảm tiểu cầu miễn dịch nguyên phát. <i>Tạp chí Nghiên cứu Y học</i>. 2025;189:247-56.",
    "Provan D, Arnold DM, Bussel JB, et al. Updated international consensus report on the investigation and management of primary immune thrombocytopenia. <i>Blood Advances</i>. 2019;3(22):3780-817.",
    "Sahi PK, Chandra J. Immune Thrombocytopenia: American Society of Hematology Guidelines, 2019. <i>Indian Pediatrics</i>. 2020;57(9):854-6.",
    "Chen Q, Zhang Y, Li Y, et al. Comparative study between two bleeding grading systems of immune thrombocytopenia purpura. <i>Hematology</i>. 2021;26(1):769-74.",
    "An ZY, Wu YJ, Hou Y, et al. A life-threatening bleeding prediction model for immune thrombocytopenia based on personalized machine learning: a nationwide prospective cohort study. <i>Science Bulletin</i>. 2023;68:2106-14.",
    "Dhiman S, Thukral A, Bedi P. An Agentic AI system for disease diagnosis with explanations. <i>Informatics and Health</i>. 2026;3:32-40.",
    "AWS Healthcare Industry Lens. Machine learning reference architecture. AWS Well-Architected Framework. 2025. Truy cập tại: docs.aws.amazon.com/wellarchitected/latest/healthcare-industry-lens/",
    "AWS Machine Learning Blog. Evaluate healthcare generative AI applications using LLM-as-a-judge on AWS. 2025.",
    "Frelinger AL, Grace RF, Gerrits AJ, et al. Platelet Function in ITP, Independent of Platelet Count, Is Consistent Over Time and Is Associated with Both Current and Subsequent Bleeding Severity. <i>Thrombosis and Haemostasis</i>. 2018;118(1):143-51.",
    "Sirotich E, Guyatt G, Gabe C, et al. Definition of a critical bleed in patients with immune thrombocytopenia: communication from the ISTH SSC Subcommittee on Platelet Immunology. <i>Journal of Thrombosis and Haemostasis</i>. 2021;19(8):2082-8.",
]

for i, ref in enumerate(references, 1):
    story.append(Paragraph(f"[{i}] {ref}", ref_style))

story.append(Spacer(1, 1*cm))

# Final closing
closing_style = ParagraphStyle(
    'Closing',
    parent=body_style,
    fontSize=11,
    leading=16,
    alignment=TA_CENTER,
    firstLineIndent=0,
    fontName='DejaVu-Italic',
    textColor=colors.HexColor('#4a5568'),
)
story.append(Paragraph(
    "Đề cương nghiên cứu này được xây dựng nhằm đáp ứng đầy đủ yêu cầu của luận "
    "văn cao học, đồng thời đóng góp một hệ thống hỗ trợ quyết định lâm sàng hiện "
    "đại, thiết thực cho thực tiễn khám chữa bệnh tại Việt Nam.",
    closing_style
))

# ============================================================
# BUILD PDF
# ============================================================

print("Building PDF...")
doc.build(story)
print(f"PDF created: {output_path}")

import os
size_kb = os.path.getsize(output_path) / 1024
print(f"Size: {size_kb:.1f} KB")
