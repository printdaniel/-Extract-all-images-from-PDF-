from tkinter import *
from tkinter.font import BOLD
from tkinter import filedialog
from tkinter import messagebox
import fitz
import io
import os
from PIL import Image
import zipfile

class photopdf:
    def __init__(self,window):
        self.root=window
        self.root.title("foto-extractor de PDF")
        self.root.config(bg="#f8e91a")


        frame = LabelFrame(self.root, text = 'Panel de datos',bg='#578D2F', padx=20, pady=30)
        frame.grid(row=0,column=0,padx=10,pady=10)


        btn_open = Button(frame, text='Abrir Archivo',padx=5, pady=5,bg='#836F41',width=12,command=self.open)
        btn_open.grid(row=0,column=0)

        btn_conv = Button(frame, text='Extraer imagenes',padx=5, pady=5,bg='#836F41',width=12,command=self.eject)
        btn_conv.grid(row=1,column=0)
        
        
    def open(self):
        global ruta,archivo
    
        self.root.filename = filedialog.askopenfilename(initialdir = "/",title = "Selecionar Archivo",filetypes = (("pdf files","*.pdf"),("all files","*.*")))
        sep = self.root.filename.split(sep='/')
        
        dire = sep[:-1]
        ruta ='/'.join(dire)
        
        archivo = sep[-1]
        print(ruta,archivo)
        
        return ruta,archivo
    
    
    def eject(self):
        print(ruta,archivo)
        while True:
            print("------------------PDF IMAGE EXTRACTOR------------------\n")
            
            
            os.chdir(ruta)
            
            images = []
 
            pdf_file = fitz.open(archivo)
            print('{} Páginas'.format(len(pdf_file)))
            for page_index in range(len(pdf_file)):
                page = pdf_file[page_index]
                image_list = page.getImageList()
                print('{} imágenes encontradas en la página {}'.format(len(image_list),page_index))
 
                for image_index, img in enumerate(page.getImageList(), start=1):
                    xref = img[0]
                    base_image = pdf_file.extractImage(xref)
                    image_bytes = base_image["image"]
                    image_ext = base_image["ext"]
                    image = Image.open(io.BytesIO(image_bytes))
                    image_name = (f"image{page_index+1}_{image_index}.{image_ext}")
                    image.save(open(image_name,"wb"))
                    images.append(image_name)
            folder_name, ex = os.path.splitext(archivo)
 
            with zipfile.ZipFile(folder_name+".zip","w") as zfile:
                for i in images:
                    zfile.write(i)
                    os.remove(i)
            zfile.close()
            print("\nCreado archivo \'{}\'.".format(folder_name+".zip"))
            messagebox.showinfo(message="Archivo "+folder_name+".zip creado con éxito")
            
            break
 
            
        
if __name__=='__main__':
    window=Tk()
    app=photopdf(window)
    window.mainloop()