//<pre>
import java.applet.*;
import java.awt.*;
import java.awt.image.*;

public class RenderApplet extends Applet implements Runnable {

private String notice = "Copyright 2001 Ken Perlin. All rights reserved.";

//--- PUBLIC DATA FIELDS

   public Shape world; // ROOT OF SCENE GEOMETRY

//--- PUBLIC METHODS

   public void animate(double time) { isDamage = false; } // OVERRIDE TO ANIMATE
   public void damage() { isDamage = true; }                   // FORCE A RERENDER
   public void setFOV(double value) { renderer.setFOV(value); }// SET FIELD OF VIEW
   public void setFL(double value) { renderer.setFL(value); }  // SET FOCAL LENGTH
   public void setBgColor(double r, double g, double b) {      // SET BACKGROUND COLOR
      renderer.setBgColor(r, g, b);
   }
   public void addLight(double x,double y,double z,            // ADD A LIGHT SOURCE
			double r,double g,double b) {
      renderer.addLight(x, y, z, r, g, b);
   }

   // PUBLIC METHODS TO LET THE PROGRAMMER MANIPULATE A MATRIX STACK

   public void identity() { Matrix.identity(m()); }
   public double[][] m() { return m[top]; }
   public void pop() { top--; }
   public void push() { Matrix.copy(m[top],m[top+1]); top++; }
   public void rotateX(double t) { Matrix.rotateX(m(), t); }
   public void rotateY(double t) { Matrix.rotateY(m(), t); }
   public void rotateZ(double t) { Matrix.rotateZ(m(), t); }
   public void scale(double x,double y,double z) { Matrix.scale(m(),x,y,z); }
   public void transform(Shape s) { s.setMatrix(m()); }
   public void translate(double x,double y,double z) {
      Matrix.translate(m(), x, y, z);
   }

//--- SYSTEM LEVEL PUBLIC METHODS ---

   public void init() {
       W = getBounds().width;
       H = getBounds().height;
       renderer = new Renderer();
       mis = new MemoryImageSource(W, H, renderer.init(W,H), 0, W);
       mis.setAnimated(true);
       im = createImage(mis);
       startTime = getCurrentTime();
       world = renderer.getWorld(); // GET ROOT OF GEOMETRY
       identity();
       initialize();
   }

   public void initialize() { } // APPLICATION PROGRAM OVERRIDES THIS

   public void start() {
      if (t == null) {
         t = new Thread(this);
         t.start();
      }
   }
   public void stop() {
      if (t != null) {
         t.stop();
         t = null;
      }
   }
   public void run() {
      int o = 0;
      while(true) {

         // MEASURE ELAPSED TIME AND FRAMERATE

         elapsed += getCurrentTime() - currentTime;
         currentTime = getCurrentTime();

         if (isDamage) {

            frameRate = .9*frameRate + .1/elapsed;
            elapsed = 0;

	    // LET THE APPLICATION PROGRAMMER MOVE THINGS INTO PLACE

            identity();             // APPLIC. MATRIX STARTS UNTRANSFORMED
            isDamage = true;
            animate(currentTime-startTime); // APPLICATION ANIMATES THINGS

	    // SHADE AND SCAN CONVERT GEOMETRY INTO FRAME BUFFER

            renderer.render();

	    // KEEP REFINING LEVEL OF DETAIL UNTIL PERFECT (WHEN LOD=1)

            if (renderer.lod > 1) {
               isDamage = true;
               renderer.lod--;
            }

	    // WRITE RESULTS TO THE SCREEN

            mis.newPixels(0, 0, W, H, true);
            repaint();
         }
         try {
            Thread.sleep(10);
         }
         catch(InterruptedException ie) { ; }
      }
   }
   public synchronized void update(Graphics g) {
      g.drawImage(im, 0, 0, null);
      if (showFPS) {
         g.setColor(Color.white);
         g.fillRect(0,H-14,47,14);
         g.setColor(Color.black);
         g.drawString((int)frameRate + "." + ((int)(frameRate*10)%10) +
            " fps", 2, H-2);
      }
   }

//--- INTERACTIVE VIEW ROTATION EVENT CALLBACKS

   // IF MOUSE MOVES TO LOWER LEFT CORNER, THEN DISPLAY FRAME RATE

   public boolean mouseMove(Event event, int x, int y) {
      showFPS = x < 35 && y > H-14;
      return true;
   }

   // MOUSE DOWN STARTS A VIEW ROTATION

   public boolean mouseDown(Event event, int x, int y) {
      mx = x;
      my = y;
      return true;
   }

   // MOUSE DRAG MAKES VIEW ANGLE GRADUALLY ROTATE

   public boolean mouseDrag(Event event, int x, int y) {
      renderer.rotateView(0.03 * (double)(x - mx), // HORIZONTAL VIEW ROTATION
                          0.03 * (double)(y - my));// VERTICAL VIEW ROTATION
      mx = x;
      my = y;
      if (frameRate < 10 && renderer.lod < 4)
         renderer.lod++;

      isDamage = true;
      return true;
   }

//--- PRIVATE METHODS

   // GET THE CURRENT TIME IN SECONDS

   private double getCurrentTime() {
      return System.currentTimeMillis() / 1000.;
   }

//--- PRIVATE DATA FIELDS

   private Renderer renderer;          // THE RENDERER OBJECT
   private int mx, my;                 // CURRENT MOUSE POSITION
   private MemoryImageSource mis;      // THE IMAGE MEMORY SOURCE OBJECT
   private Thread t;                   // RENDERING THREAD
   private int W, H;                   // IMAGE WIDTH,HEIGHT,FRAMEBUFFER
   private Image im;                   // IMAGE CONTAINING MEMORY SOURCE OBJECT
   private boolean showFPS = false;    // SHOWING FRAME RATE? FLAG
   private double startTime = 0, currentTime = 0, elapsed = 0, frameRate = 0;
   private boolean isDamage = true;    // WHETHER WE NEED TO RECOMPUTE IMAGE
   private double m[][][] = new double[10][4][4]; // THE MATRIX STACK
   private int top = 0;                // MATRIX STACK POINTER
}

