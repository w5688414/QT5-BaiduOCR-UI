from PIL import Image

# img_path='images/56A0D0S-晋HXS199-20210803.png'
img_path='images/56A0D0S-晋HXS199-20210803.png'
# 1366x768
# img_path='images/56A0D0S-晋M00B98-20210810.png'
# img_path='images/56A0D0S-晋MD18009-20210811.png'
# 1920x1080
# img_path='images/56A0E6U-晋MN5733-20210810.png'


im = Image.open(img_path)  # 用PIL打开一个图片
print(im.size)

box = (65, 80, 290, 100)
ng = im.crop(box) 

ng.save('IMEI.png')

box = (300, 100, 600, 150)
ng = im.crop(box) 

ng.save('time1.png')

box = (300, 200, 600, 240)
ng = im.crop(box) 

ng.save('time2.png')
# x1,y1,x2,y2
box = (300, 240, 550, 260)
ng = im.crop(box) 

ng.save('mileage.png')

box = (850, 200, 1100, 240)
ng = im.crop(box) 

ng.save('mileage1.png')


# 1920x 1080

# box = (80, 100, 360, 150)
# ng = im.crop(box) 

# ng.save('IMEI.png')

# box = (400, 160, 750, 200)
# ng = im.crop(box) 

# ng.save('time1.png')

# box = (450, 250, 650, 280)
# ng = im.crop(box) 

# ng.save('time2.png')

# # # x1,y1,x2,y2
# box = (1050, 240, 1300, 280)
# ng = im.crop(box) 

# ng.save('mileage.png')

