import tkinter as tk
from tkinter import filedialog as fd
from PIL import Image, ImageTk
import numpy as np
import cv2

def __main__():
    print('2ds')
    
    global window
    global WIN_WIDTH, WIN_HEIGHT
    global IMAGE_WIDTH
    # Create main window
    window = tk.Tk()
    #
    _init_globals()
    #
    global main_win_if # Used in the func. : act_openImage()
    win_ll,win_rl,main_win_if,win_af = defaultLayout(window)
    # Action frame    
    global ACTION_BUTTONS
    for i in range(len(ACTION_BUTTONS)):
        txt,act = ACTION_BUTTONS[i]
        #
        actBtn = tk.Button(win_af,text=txt,command=act)
        actBtn.grid(row=0,column=i,sticky="nsew")
        tk.Grid.columnconfigure(win_af,i,weight=1)
    # Option frame
    global PROCESSING_BTN_ID, PROCESSING_BUTTONS
    for i in range(len(PROCESSING_BUTTONS)):
        txt,act,desc = PROCESSING_BUTTONS[i]
        #
        optBtn = tk.Radiobutton(win_rl,text=txt,anchor="w",variable=PROCESSING_BTN_ID,value=i,indicatoron=0)
        optBtn.pack(fill='x')
        descTxt = tk.Label(win_rl,text=desc,wraplength=(WIN_WIDTH-IMAGE_WIDTH),justify="left",bg="silver")
        descTxt.pack(fill='x')
    # window settings
    window.title("Sample")
    window.geometry("%dx%d"%(WIN_WIDTH,WIN_HEIGHT))
    window.resizable(width=False,height=False)
    window.mainloop()
    
def _init_globals():
    global cv2Matrix, cv2MatrixProc
    cv2Matrix = None # Image loaded with cv2.imread
    cv2MatrixProc = None # Produced image after processing
    # Main window
    global ACTION_BUTTONS
    ACTION_BUTTONS = [ # Text, Action
        ("OPEN IMAGE",  act_openImage),
        ("PROCESS",     act_process)]
    #,
    #    ("SAVE IMAGE",  act_saveImage),
    #    ("SAVE DATA",   act_saveData)
    global PROCESSING_BTN_ID, PROCESSING_BUTTONS
    PROCESSING_BTN_ID = tk.IntVar()
    PROCESSING_BUTTONS = [ # Text, Action, Description
        ("BLURRING",    proc_blurring,   "Smoothing the image."),
        ("EDGE DETECT", proc_edgeDetect, "Detect edges from image"),
        ("LINE DETECT", proc_lineDetect, "Detect lines from image using Hough Transform"),
        ("CONTOURING",  proc_contouring, "Find contours from image"),
        ("ROTATING",    proc_rotating,   "Rotate image")]
    # Processed window
    global proc_window
    proc_window = None
    global PROC_ACTION_BUTTONS
    PROC_ACTION_BUTTONS = [ # Text, Action
        ("APPLY",       procAct_apply),
        ("SAVE IMAGE",  procAct_saveImage),
        ("SAVE DATA",   procAct_saveData)]
    # Window sizing config.
    global WIN_WIDTH, WIN_HEIGHT
    WIN_WIDTH  = 540
    WIN_HEIGHT = 480
    global LAYOUT_L_WIDTH, LAYOUT_R_WIDTH
    LAYOUT_L_WIDTH  = 400
    LAYOUT_R_WIDTH  = WIN_WIDTH-LAYOUT_L_WIDTH
    global IMAGE_WIDTH, IMAGE_HEIGHT, BUTTON_HEIGHT
    BUTTON_HEIGHT   = 26
    IMAGE_WIDTH     = LAYOUT_L_WIDTH
    IMAGE_HEIGHT    = WIN_HEIGHT-BUTTON_HEIGHT

def readUnicodePath(path):
    stream = open(path,"rb")
    bytes = bytearray(stream.read())
    numpyArray = np.asarray(bytes,dtype=np.uint8)
    img_bgr = cv2.imdecode(numpyArray, cv2.IMREAD_UNCHANGED)
    return img_bgr

def createImageFrame(master,width,height,*args,**kwargs):
    f = tk.Frame(master,width=width,height=height)
    f.pack_propagate(0) # Disable shrink/expand
    f.pack()
    l = tk.Label(f,bg="black",*args,**kwargs)
    l.pack(fill="both",expand=1)
    return l

def defaultLayout(master):    
    global WIN_WIDTH, WIN_HEIGHT
    global LAYOUT_L_WIDTH, LAYOUT_R_WIDTH
    global IMAGE_WIDTH, IMAGE_HEIGHT, BUTTON_HEIGHT
    ### Root
    leftLayout = tk.Frame(master,width=LAYOUT_L_WIDTH,height=WIN_HEIGHT)
    leftLayout.pack_propagate(False)
    leftLayout.pack(side="left",fill=None,expand=False)
    rightLayout = tk.Frame(master)
    rightLayout.pack(side="left",fill="both",expand=1)
    # Image frame
    imageFrame = createImageFrame(leftLayout,IMAGE_WIDTH,IMAGE_HEIGHT)
    # Action frame
    actionFrame = tk.Frame(leftLayout,height=BUTTON_HEIGHT)
    actionFrame.pack(fill="x",expand=1)
    #
    return leftLayout, rightLayout, imageFrame, actionFrame

def show_image(imageFrame, image):
    global IMAGE_WIDTH, IMAGE_HEIGHT
    # Exception; Image not loaded
    if image is None:
        print("No Image")
        return
    # calc image size
    h,w,ch = image.shape
    imageWidth  = int(IMAGE_WIDTH)
    imageHeight = int(IMAGE_WIDTH*(h/w))
    if imageHeight > IMAGE_HEIGHT:
        imageHeight = int(IMAGE_HEIGHT)
        imageWidth  = int(IMAGE_HEIGHT*(w/h))
    manualSize = (imageWidth,imageHeight)
    # image resize & convert
    improc = cv2.resize(image.copy(),manualSize,interpolation=cv2.INTER_AREA)
    improc = cv2.cvtColor(improc,cv2.COLOR_BGR2RGB)
    improc = Image.fromarray(improc)
    improc = ImageTk.PhotoImage(improc)
    # apply image
    imageFrame.configure(image=improc)
    imageFrame.image=improc

# ACTIONS
def act_openImage():
    global cv2Matrix
    global main_win_if
    fname = fd.askopenfilename()
    # Exception; Canceled by user
    if fname == "":
        return
    # cv2Matrix = cv2.imread(fname) # ERROR : Cannot read unicode folder names
    cv2Matrix = readUnicodePath(fname)
    # Exception; File not found
    if cv2Matrix is None:
        print("Could not find file named '%s'"%fname)
        return
    #
    show_image(main_win_if,cv2Matrix)

def act_process():
    global window, proc_window
    global WIN_WIDTH, WIN_HEIGHT
    global PROCESSING_BTN_ID, PROCESSING_BUTTONS
    global proc_selectedProc
    global proc_win_rl, proc_win_if
    global PROC_ACTION_BUTTONS
    # Destroy existing window
    if not (proc_window is None):
        proc_window.destroy()
    # Memorize called process
    proc_selectedProc = PROCESSING_BUTTONS[PROCESSING_BTN_ID.get()][1]
    # Build new window
    proc_window = tk.Toplevel(window)
    proc_window.title("Processed Image")
    proc_window.geometry("%dx%d"%(IMAGE_WIDTH+200,WIN_HEIGHT))
    win_ll,proc_win_rl,proc_win_if,win_af = defaultLayout(proc_window)
    # Action frame
    for i in range(len(PROC_ACTION_BUTTONS)):
        txt,act = PROC_ACTION_BUTTONS[i]
        #
        actBtn = tk.Button(win_af,text=txt,command=act)
        actBtn.grid(row=0,column=i,sticky="nsew")
        tk.Grid.columnconfigure(win_af,i,weight=1)
    # Process the image
    procAct_apply()

# PROCESSING
class Dataset:
    def __init__(self,master,setName):
        self.name = setName
        self.dataset = []
        self.radioVar = tk.StringVar()
        #
        self._setFrame = tk.Frame(master)
        self._setFrame.pack(fill="x",expand=1)
        l = tk.Label(self._setFrame,text=self.name,anchor="nw",bg="silver")
        l.pack(fill="x",expand=1)

    def _newData(self,valueName):
        global LAYOUT_R_WIDTH
        lineFrame = tk.Frame(self._setFrame,padx=4)
        lineFrame.pack(fill="x",expand=1)
        labelFrame = tk.Frame(lineFrame,width=160,height=28)
        labelFrame.pack_propagate(0)
        labelFrame.pack(side="left")
        label = tk.Label(labelFrame,text=valueName,anchor="w")
        label.pack(fill="both",expand=1)
        return lineFrame

    def getData(self,index):
        type,widget,get = self.dataset[i]
        if type is "Checkbutton":
            return get()

    def entry(self,valueName,value):
        lineFrame = self._newData(valueName)
        entry = tk.Entry(lineFrame)
        entry.pack(side="left",fill="x",expand=1)
        entry.insert(0,str(value))
        #
        self.dataset.append(("Entry",entry,entry.get))
        return entry

    def checkbutton(self,valueName,value):
        lineFrame = self._newData(valueName)
        v = tk.BooleanVar()
        btn = tk.Checkbutton(lineFrame,text=str(value),var=v,indicatoron=0)
        btn.pack(side="left",fill="x",expand=1)
        #
        self.dataset.append(("Checkbutton",btn,v.get))
        return btn

    def radiobutton(self,valueName,value):
        lineFrame = self._newData(valueName)
        btn = tk.Radiobutton(lineFrame,text="",variable=self.radioVar,value=value,indicatoron=0)
        btn.pack(side="left",fill="x",expand=1)
        #
        self.dataset.append(("Radiobutton",btn,self.radioVar.get))
        return btn

def proc_blurring(image):
    return image

def proc_edgeDetect(image):
    return image

def proc_lineDetect(image):
    global proc_win_rl
    # Smoothing
    GAUSS_KERNEL = (3,3)
    GAUSS_SIGMA = 25
    src = cv2.GaussianBlur(image.copy(), GAUSS_KERNEL, GAUSS_SIGMA)
    # Canny Edge
    canny = cv2.Canny(src, 50, 150, apertureSize=3)
    lines = cv2.HoughLines(canny, 1, np.pi/180, 100)
    
    canvas = image.copy()
    
    d = Dataset(proc_win_rl,setName="Hough Line Trans. (rho, theta)")
    for line in lines:
        for rho,theta in line:
            chkBtn = d.checkbutton("(%lf, %lf)"%(rho,theta), "")
            # Draw Lines
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a*rho
            y0 = b*rho
            x1 = int(x0 +1000*(-b))
            y1 = int(y0 +1000*(a))
            x2 = int(x0 -1000*(-b))
            y2 = int(y0 -1000*(a))
            cv2.line(canvas,(x1,y1),(x2,y2),(0,0,255),1)
    return canvas

def proc_contouring(image):
    global proc_win_rl
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    # Smoothing
    d = Dataset(proc_win_rl,'Smoothing')
    GAUSS_KERNEL_SIZE = 3
    GAUSS_SIGMA = 25
    blurred = cv2.GaussianBlur(gray, (GAUSS_KERNEL_SIZE,GAUSS_KERNEL_SIZE), GAUSS_SIGMA)
    d.entry('kernel size', GAUSS_KERNEL_SIZE)
    d.entry('sigma', GAUSS_SIGMA)
    # Thresholding
    THRESH = 240
    d.entry('threshold', THRESH)
    ret, threshed = cv2.threshold(blurred, THRESH, 255, cv2.THRESH_BINARY_INV)
    # Morphology-OPENING operation to remove extra noises
    threshed = cv2.morphologyEx(threshed,cv2.MORPH_OPEN,(5,5),iterations=10)
    # Find & draw contours
    contours, hierarchy = cv2.findContours(threshed, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)    
    canvas = np.zeros(image.shape, np.uint8)
    for cont in contours:
        cv2.drawContours(canvas, [cont], 0, (255,255,255), 1)
    return canvas

def proc_rotating(image):
    global proc_win_rl
    d = Dataset(proc_win_rl,setName="Possible thetas")
    for i in range(8):
        radBtn = d.radiobutton("%d (%.2f%%)"%(i*15,100/8), "%d"%(i*15))
    return image

# AFTER-PROCESSING ACTIONS
def procAct_apply():
    global cv2Matrix, cv2MatrixProc
    global proc_selectedProc
    cv2MatrixProc = proc_selectedProc(cv2Matrix)
    show_image(proc_win_if,cv2MatrixProc)

def procAct_saveImage():
    pass

def procAct_saveData():
    pass