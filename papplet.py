from gi.repository import Rsvg,Gtk,GLib,Gdk
import svgwrite

def is_in(x,y,box):
    x1,y1,x2,y2=box
    if x<=max(x1,x2) and x>=min(x1,x2) and y<=max(y1,y2) and y>=min(y1,y2):
        return True
    return False

class PApplet(Gtk.Window):
    def __init__(self,title=None,height=500,width=500,framerate=20):
        Gtk.Window.__init__(self,title=title)
        self.height=height
        self.width=width
        self.dwg=svgwrite.container.SVG(size=(width,height),debug=False)
        self.canvas=Gtk.Image().new_from_pixbuf(Rsvg.Handle().new_from_data(bytes(self.dwg.tostring(),'ascii')).get_pixbuf())
        self.add(self.canvas)
        self.framerate=framerate
        #self.timeout=GLib.timeout_add(1000//framerate,self._draw)
        self.idle=None
        self.add_events(Gdk.EventMask.POINTER_MOTION_MASK)
        self.connect("delete-event",self.cleanup)
        self.connect("motion-notify-event",self.motion)
        self.mouseX=0
        self.mouseY=0
        self.add_events(Gdk.EventMask.KEY_PRESS_MASK)
        self.connect("key-press-event",self._keypress)
        self.add_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        self.connect("button_press_event",self._mousedown)
        self.keydown=None
        self.mouseclicked=None
        self.mousedown=False
        
    def __enter__(self):
        return self
    def __exit__(self,exc_type,exc_value,traceback):
        self.cleanup(None,None)
    def _mousedown(self,widget,event):
        self.on_mousedown()
    def on_mousedown(self):
        pass
    def _keypress(self,widget,event):
        self.keydown=event.keyval
        self.on_keypress()
        #self.keydown=None
        return True
    def on_keypress(self):
        pass#user defined callback
    def start(self):
        self.idle=GLib.idle_add(self._draw)
        self.setup()
        Gtk.main()
        
        
    def setup(self):
        pass
    def draw(self):
		#user defined actions
        pass
    def _draw(self):
        self.remove(self.canvas)
        self.draw()
        self.canvas=Gtk.Image().new_from_pixbuf(Rsvg.Handle().new_from_data(bytes(self.dwg.tostring(),'ascii')).get_pixbuf())
        self.add(self.canvas)
        self.show_all()
        return True
    def cleanup(self,widget,event):
        #GLib.Source().remove(self.timeout)
        if self.idle:
            GLib.Source().remove(self.idle)
        Gtk.main_quit()
    def motion(self,widget,event):
        state=event.state
        if (state&Gdk.EventMask.BUTTON_PRESS_MASK):
            self.mousedown=True
        else:
            self.mousedown=False
        self.mouseX=event.x
        self.mouseY=event.y
        self.mousemove()
    def mousemove(self):
        pass


