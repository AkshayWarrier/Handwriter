from PIL import Image, ImageDraw
import cv2
import numpy


alpha = [Image.open('assets//'+chr(x)+'.jpg') for x in range(97,123)]
alpha_cap = [Image.open('assets//'+chr(x)+'cap.jpg') for x in range(65,91)]
scale = 0.75

for i in range(len(alpha)):
   alpha[i] = alpha[i].resize((int(alpha[i].width*scale),int(alpha[i].height*scale)))
#264 approx height of character
#12 lines in one page

def writeline(line_no,text,im):
    x = 0
    y = int(line_no*264*scale)
    for i in range(len(text)):   
        if text[i].isalpha():
            if text[i].islower():
                char_img = alpha[ord(text[i])-97]
            else:
                char_img = alpha_cap[ord(text[i])-65]
            x += char_img.width
            if x >= 2480:
                line_no += 1
                y = int(line_no*264*scale)
                x = 0
                Image.Image.paste(im,char_img,(x,y))
                x += char_img.width
            else:
                Image.Image.paste(im,char_img,(x - char_img.width ,y))
        else:
            if text[i] == ' ':
                x += int(70*scale)
                if x >= 2480:
                    line_no += 1
                    y = int(line_no*264*scale)
                    x = 70
                else:
                    pass
            elif text[i] == '.':
                draw = ImageDraw.Draw(im)
                draw.ellipse([x,y,x+20,y+264],fill = 'black',outline='black')
                x += 10
            elif text[i] == '\n':
                line_no += 1
                y = int(line_no*264*scale)
                x = 0
            elif text[i] == '\x08':
                if text[-1].isupper():
                    x -= alpha_cap[ord(text[-1])-97].width
                elif text[-1].islower():
                    x -= alpha[ord(text[-1])-97].width
                    arr = numpy.array(im)
                    print(arr[x:x+im.width,y:y+im.height])
                    arr[y:y+im.height,x:x+im.width] = (255,255,255)
                    im = Image.fromarray(arr)
                text = text[0:-2]
                return text


# l = list("abcdefghijklmnopqrstuvwxyz")
# shuffle(l)
text = ""


im = Image.new('RGB',(2480,3508))
canvas = ImageDraw.Draw(im)
canvas.rectangle([(0,0),(2480,3508)],fill=(255,255,255))


im_arr = numpy.array(im)
# im_arr = im_arr[:, :, ::-1].copy() 
cv2.namedWindow("output", cv2.WINDOW_NORMAL)
cv2.resizeWindow("output",620 ,877)
while True:
    cv2.imshow('output',im_arr)
    inp = cv2.waitKey(0)
    if inp == ord('/'):
        cv2.destroyAllWindows()
        break
    elif inp != '':
        if inp == 8:
            text += '\x08'
            # print(text)
            text = writeline(0,text,im)
            im_arr = numpy.array(im)
        else:
            text += chr(inp)
            writeline(0,text,im)
            im_arr = numpy.array(im)



