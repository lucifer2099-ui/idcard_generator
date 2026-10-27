import os
import secrets
secure_random = secrets.SystemRandom()
import sys
import threading
import tkinter
from tkinter.filedialog import *
from tkinter.messagebox import *
from tkinter.ttk import *

import PIL.Image as PImage
import cv2
import numpy
from PIL import ImageFont, ImageDraw

from idcard_generator import id_card_utils, name_utils, utils, loading_alert, address_utils

asserts_dir = os.path.join(utils.get_base_path(), 'asserts')
print("asserts_dir", asserts_dir)


def set_entry_value(entry, value):
    entry.delete(0, tkinter.END)
    entry.insert(0, value)


def change_background(img, img_back, zoom_size, center):
    # 缩放
    img = cv2.resize(img, zoom_size)
    rows, cols, channels = img.shape

    # 转换hsv
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # 获取mask
    # lower_blue = np.array([78, 43, 46])
    # upper_blue = np.array([110, 255, 255])
    diff = [5, 30, 30]
    gb = hsv[0, 0]
    lower_blue = numpy.array(gb - diff)
    upper_blue = numpy.array(gb + diff)
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    # cv2.imshow('Mask', mask)

    # 腐蚀膨胀
    erode = cv2.erode(mask, None, iterations=1)
    dilate = cv2.dilate(erode, None, iterations=1)

    # 粘贴
    bool_mask = (dilate == 0)
    img_back[center[0]:center[0]+rows, center[1]:center[1]+cols][bool_mask] = img[bool_mask]

    return img_back


def paste(avatar, bg, zoom_size, center):
    avatar = cv2.resize(avatar, zoom_size)
    rows, cols, channels = avatar.shape
    bg[center[0]:center[0]+rows, center[1]:center[1]+cols] = avatar
    return bg


class IDGen:
    def random_data(self):
        random_name = name_utils.random_name()
        set_entry_value(self.eName, random_name["name_full"])
        set_entry_value(self.eSex, '女' if random_name['sex'] == 0 else "男")
        set_entry_value(self.eNation, "汉")
        year = secure_random.randint(1980, 1995)
        set_entry_value(self.eYear, year)
        month = secure_random.randint(1, 12)
        set_entry_value(self.eMon, month)
        day = id_card_utils.random_day(year, month)
        set_entry_value(self.eDay, day)
        set_entry_value(self.eAddr, address_utils.get_random_address())
        set_entry_value(self.eIdn, id_card_utils.random_card_no(year=str(year), month=str(month), day=str(day), sex=random_name['sex']))
        set_entry_value(self.eOrg, "江苏省徐州市鼓楼分局")
        start_time, expire_time = id_card_utils.generate_validity_period()
        set_entry_value(self.eLife, start_time + "-" + expire_time)

    def generator_image(self):
        self.f_name = askopenfilename(initialdir=os.getcwd(), title='选择头像')
        if len(self.f_name) == 0:
            return

        self.loading_bar = loading_alert.LoadingBar(title="提示", content="图片正在生成...")
        self.loading_bar.show(self.root)

        # 开启新线程保持滚动条显示
        wait_thread = threading.Thread(target=self.handle_image)
        wait_thread.setDaemon(True)
        wait_thread.start()

    def handle_image(self):
        avatar = PImage.open(self.f_name)  # 500x670
        empty_image = PImage.open(os.path.join(asserts_dir, 'empty.png'))

        name_font = ImageFont.truetype(os.path.join(asserts_dir, 'fonts/hei.ttf'), 72)
        other_font = ImageFont.truetype(os.path.join(asserts_dir, 'fonts/hei.ttf'), 64)
        birth_date_font = ImageFont.truetype(os.path.join(asserts_dir, 'fonts/fzhei.ttf'), 60)
        id_font = ImageFont.truetype(os.path.join(asserts_dir, 'fonts/ocrb10bt.ttf'), 90)

        draw = ImageDraw.Draw(empty_image)
        draw.text((630, 690), self.eName.get(), fill=(0, 0, 0), font=name_font)
        draw.text((630, 840), self.eSex.get(), fill=(0, 0, 0), font=other_font)
        draw.text((1030, 840), self.eNation.get(), fill=(0, 0, 0), font=other_font)
        draw.text((630, 975), self.eYear.get(), fill=(0, 0, 0), font=birth_date_font)
        draw.text((950, 975), self.eMon.get(), fill=(0, 0, 0), font=birth_date_font)
        draw.text((1150, 975), self.eDay.get(), fill=(0, 0, 0), font=birth_date_font)

        # 住址
        addr_loc_y = 1115
        addr_lines = self.get_addr_lines()
        for addr_line in addr_lines:
            draw.text((630, addr_loc_y), addr_line, fill=(0, 0, 0), font=other_font)
            addr_loc_y += 100

        # 身份证号
        draw.text((900, 1475), self.eIdn.get(), fill=(0, 0, 0), font=id_font)

        # 背面
        draw.text((1050, 2750), self.eOrg.get(), fill=(0, 0, 0), font=other_font)
        draw.text((1050, 2895), self.eLife.get(), fill=(0, 0, 0), font=other_font)

        if self.eBgvar.get():
            avatar = cv2.cvtColor(numpy.asarray(avatar), cv2.COLOR_RGBA2BGRA)
            empty_image = cv2.cvtColor(numpy.asarray(empty_image), cv2.COLOR_RGBA2BGRA)
            empty_image = change_background(avatar, empty_image, (500, 670), (690, 1500))
            empty_image = PImage.fromarray(cv2.cvtColor(empty_image, cv2.COLOR_BGRA2RGBA))
        else:
            avatar = avatar.resize((500, 670))
            avatar = avatar.convert('RGBA')
            empty_image.paste(avatar, (1500, 690), mask=avatar)
            # im = paste(avatar, im, (500, 670), (690, 1500))

        empty_image.save('color.png')
        empty_image.convert('L').save('bw.png')

        self.loading_bar.close()
        showinfo('成功', '文件已生成到目录下,黑白bw.png和彩色color.png')

    def _create_label_entry(self, root, label_text, row, col, width, columnspan=1):
        Label(root, text=label_text).grid(row=row, column=col, sticky=tkinter.W, padx=3, pady=3)
        entry = Entry(root, width=width)
        entry.grid(row=row, column=col + 1, sticky=tkinter.W, padx=3, pady=3, columnspan=columnspan)
        return entry

    def show_ui(self, root):
        self.root = root
        root.title('AIRobot身份证图片生成器')
        root.resizable(width=False, height=False)
        link = Label(root, text='请遵守法律法规，获取帮助:', cursor='hand2', foreground="#FF0000")
        link.grid(row=0, column=0, sticky=tkinter.W, padx=3, pady=3, columnspan=3)
        link.bind("<Button-1>", utils.open_url)

        link = Label(root, text='https://github.com/bzsome', cursor='hand2', foreground="blue")
        link.grid(row=0, column=2, sticky=tkinter.W, padx=26, pady=3, columnspan=4)
        link.bind("<Button-1>", utils.open_url)

        self.eName = self._create_label_entry(root, '姓名:', 1, 0, width=8)
        self.eSex = self._create_label_entry(root, '性别:', 1, 2, width=8)
        self.eNation = self._create_label_entry(root, '民族:', 1, 4, width=8)

        self.eYear = self._create_label_entry(root, '出生年:', 2, 0, width=8)
        self.eMon = self._create_label_entry(root, '月:', 2, 2, width=8)
        self.eDay = self._create_label_entry(root, '日:', 2, 4, width=8)

        self.eAddr = self._create_label_entry(root, '住址:', 3, 0, width=32, columnspan=5)
        self.eIdn = self._create_label_entry(root, '证件号码:', 4, 0, width=32, columnspan=5)
        self.eOrg = self._create_label_entry(root, '签发机关:', 5, 0, width=32, columnspan=5)
        self.eLife = self._create_label_entry(root, '有效期限:', 6, 0, width=32, columnspan=5)

        Label(root, text='选项:').grid(row=7, column=0, sticky=tkinter.W, padx=3, pady=3)
        self.eBgvar = tkinter.IntVar()
        self.eBgvar.set(1)
        self.ebg = Checkbutton(root, text='自动抠图', variable=self.eBgvar)
        self.ebg.grid(row=7, column=1, sticky=tkinter.W, padx=3, pady=3, columnspan=5)

        random_btn = Button(root, text='随机', width=8, command=self.random_data)
        random_btn.grid(row=8, column=0, sticky=tkinter.W, padx=16, pady=3, columnspan=2)
        generator_btn = Button(root, text='选择头像并生成', width=24, command=self.generator_image)
        generator_btn.grid(row=8, column=2, sticky=tkinter.W, padx=1, pady=3, columnspan=4)

        # 触发随机生成
        self.random_data()

    # 获得要显示的住址数组
    def get_addr_lines(self):
        addr = self.eAddr.get()
        addr_lines = []
        start = 0
        while start < utils.get_show_len(addr):
            show_txt = utils.get_show_txt(addr, start, start + 22)
            addr_lines.append(show_txt)
            start = start + 22

        return addr_lines

    def run(self):
        root = tkinter.Tk()
        self.show_ui(root)
        ico_path = os.path.join(asserts_dir, 'ico.ico')
        root.iconbitmap(ico_path)
        root.protocol('WM_DELETE_WINDOW', lambda: sys.exit(0))
        root.mainloop()
