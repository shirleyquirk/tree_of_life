#from gi.repository import Rsvg,Gtk,GLib,Gdk
import svgwrite

class PApplet:#(Gtk.Window):
    def __init__(self,title=None,height=500,width=500,framerate=20):
        #Gtk.Window.__init__(self,title=title)
        self.height=height
        self.width=width
        self.dwg=svgwrite.container.SVG(size=(width,height),debug=False)
        #self.canvas=Gtk.Image().new_from_pixbuf(Rsvg.Handle().new_from_data(bytes(self.dwg.tostring(),'ascii')).get_pixbuf())
        #self.add(self.canvas)
        self.framerate=framerate
        #self.timeout=GLib.timeout_add(1000//framerate,self._draw)
        self.idle=None
        #self.add_events(Gdk.EventMask.POINTER_MOTION_MASK)
        #self.connect("delete-event",self.cleanup)
        #self.connect("motion-notify-event",self.motion)
        self.mouseX=200
        self.mouseY=500
        #self.add_events(Gdk.EventMask.KEY_PRESS_MASK)
        #self.connect("key-press-event",self._keypress)
        self.keydown=None
    def __enter__(self):
        return self
    def __exit__(self,exc_type,exc_value,traceback):
        self.cleanup(None,None)
    def _keypress(self,widget,event):
        self.keydown=event.keyval
        self.on_keypress()
        #self.keydown=None
        return True
    def on_keypress(self):
        pass#user defined callback
    def start(self):
        #self.idle=GLib.idle_add(self._draw)
        pass
        #Gtk.main()
        
    def draw(self):
		#user defined actions
        pass
    def _draw(self):
        #self.remove(self.canvas)
        self.dwg=svgwrite.container.SVG(size=(self.width,self.height),debug=False)
        self.draw()
        #self.canvas=Gtk.Image().new_from_pixbuf(Rsvg.Handle().new_from_data(bytes(self.dwg.tostring(),'ascii')).get_pixbuf())
        #self.add(self.canvas)
        #self.show_all()
        return True
    def cleanup(self,widget,event):
        #GLib.Source().remove(self.timeout)
        pass
        #if self.idle:
            #GLib.Source().remove(self.idle)
        #Gtk.main_quit()
    def motion(self,widget,event):
        #self.mouseX=event.x
        #self.mouseY=event.y
        pass

