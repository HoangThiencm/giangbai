from PIL import Image

pages_order = [
    (1, 'page_1_Im5.jpg', 'page_1_Im6.jpg'),
    (2, 'page_2_Im9.jpg', 'page_2_Im10.jpg'),
    (3, 'page_3_Im13.jpg', 'page_3_Im14.jpg'),
    (4, 'page_4_Im17.jpg', 'page_4_Im18.jpg')
]

for pnum, top_name, bot_name in pages_order:
    top = Image.open(f'GIAO AN/FILE BAI HOC/extracted_pages/{top_name}')
    bot = Image.open(f'GIAO AN/FILE BAI HOC/extracted_pages/{bot_name}')
    full = Image.new('RGB', (top.width, top.height + bot.height))
    full.paste(top, (0, 0))
    full.paste(bot, (0, top.height))
    full.save(f'GIAO AN/hinh_anh/page_{pnum}_stitched.png')
    print(f'Page {pnum} stitched: {full.size}')

print("All 4 pages stitched successfully!")
