class Element:
    def __init__(self,element):
        self.property =element["modifiers"]
        self.element=element
        self.link=False
        self.orderlist=False
        self.unorderlist=False
        self.image=False
        self.classes=""
        self.text=""
        self.url=""
        self.setElement()
    def setElement(self):
        style=self.property.keys()
        self.text=self.element["text"]
        if "bold" in style:
            self.classes+=" fw-bolder"
        if "italic" in style:
            self.classes+=" fst-italic"
        if "link" in style  or "embed" in style:
            self.link=True
            if "link" in style:
                self.url=self.property["link"]["url"]
            else:
                self.text=self.property["embed"]["snippet"]
                self.url=self.property["embed"]["url"]
        if "image" in style:
            self.image=True
            self.url=self.property["image"]
    def createElement(self):
        
        if self.link:
            child=f"<a href={self.url}>"+self.text+"</a>"
        elif self.image:
            child=f"<img src={self.url}>"
        else:
            child=self.text
        return f"<span class={self.classes}>"+child +"</span>"