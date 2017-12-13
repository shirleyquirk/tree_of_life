//<pre>
public class Renderer {

private String notice = "Copyright 2001 Ken Perlin. All rights reserved.";

   public int lod = 1;                // LEVEL OF DETAIL FOR MESHES

//--- PUBLIC METHODS

   // INITIALIZE THE RENDERER

   public int[] init(int W, int H) {
       this.W = W;
       this.H = H;
       Matrix.identity(camera);
       pix = new int[W*H];
       return pix;
   }

   // SET THE FOCAL LENGTH

   public void setFL(double value) { FL = value; }

   // SET THE FOCAL OF VIEW

   public void setFOV(double value) { FOV = value; }

   // GET THE ROOT OF THE GEOMETRY TREE

   public Shape getWorld() { return world; }

   // SET THE BACKGROUND FILL COLOR

   public void setBgColor(double r, double g, double b) {
      bgColor = pack(f2i(r), f2i(g), f2i(b));
   }

   // ADD A LIGHT SOURCE FROM DIRECTION (x,y,z) WITH COLOR (r,g,b)

   public void addLight(double x,double y,double z,
                        double r,double g,double b) {
      double s = Math.sqrt(x*x + y*y + z*z);
      light[nLights][0] = x/s;
      light[nLights][1] = y/s;
      light[nLights][2] = z/s;
      light[nLights][3] = r;
      light[nLights][4] = g;
      light[nLights][5] = b;
      nLights++;
   }

   // SHIFT ANGLE OF VIEW

   public synchronized void rotateView(double t, double p) {
      theta += t;
      phi   += p;
   }

   // RENDER THE ENTIRE WORLD FOR THIS FRAME

   public synchronized void render() {

      computeCamera(); // UPDATE CAMERA MATRIX
      clearScreen();   // BLANK OUT RESULTS FROM PREVIOUS FRAME
      renderWorld();   // RENDER EVERYTHING IN SCENE
   }

//------------------- PRIVATE METHODS ---------------------

   // CONVERT PIXEL (X,Y) TO INDEX INTO pix ARRAY

   private int xy2i(int x, int y) { return y * W + x; }

   // CONVERT FLOATING POINT TO 0..255 INTEGER

   private int f2i(double t) {
      return (int)(255 * t) & 255;
   }

   // PACK RGB INTO ONE WORD

   private int pack(int r, int g, int b) {
      return r << 16 | g << 8 | b | 0xff000000;
   }

   // UNPACK RGB OUT OF ONE WORD

   private void unpack(int rgb[], int packed) {
      rgb[0] = (packed >> 16) & 255;
      rgb[1] = (packed >>  8) & 255;
      rgb[2] = (packed      ) & 255;
   }

   // FILL A RECTANGLE WITH A COLOR

   private void fill(int x, int y, int w, int h, int packed) {
      for (int Y = y ; Y < y + h ; Y++) {
         int i = xy2i(x, Y);
         for (int X = x ; X < x + w ; X++)
            pix[i++] = packed;
      }
   }

   // CLEAR DAMAGED PART OF SCREEN

   private void clearScreen() {
      if (TOP == -1) {
         LEFT   = 0;
         RIGHT  = W-1;
         TOP    = 0;
         BOTTOM = H-1;
      }

      LEFT   = Math.max(LEFT  , 0  );
      RIGHT  = Math.min(RIGHT , W-1);
      TOP    = Math.max(TOP   , 0  );
      BOTTOM = Math.min(BOTTOM, H-1);

      fill(LEFT, TOP, 1+RIGHT-LEFT, 1+BOTTOM-TOP, bgColor);

      if (zbuffer == null)
         zbuffer = new int[W*H];
      for (int y = TOP ; y <= BOTTOM ; y++) {
         int i = xy2i(LEFT, y);
         for (int x = LEFT ; x <= RIGHT ; x++)
            zbuffer[i++] = -zHuge;
      }

      LEFT   = W+1;
      RIGHT  =  -1;
      TOP    = H+1;
      BOTTOM =  -1;
   }

   // CALLED IN RENDER THREAD TO RECOMPUTE CAMERA VALUE

   private synchronized void computeCamera() {

      if (theta == 0 && phi == 0)
         return;

      Matrix.identity(camtmp);
      Matrix.rotateY(camtmp, theta);
      Matrix.postMultiply(camera, camtmp);

      Matrix.identity(camtmp);
      Matrix.rotateX(camtmp, phi);
      Matrix.postMultiply(camera, camtmp);

      Matrix.identity(camtmp);
      Matrix.rotateZ(camtmp, .3 * Math.atan2(camera[0][1],camera[1][1]));
      Matrix.postMultiply(camera, camtmp);

      theta = phi = 0; // WE'VE ACCOUNTED FOR ROTATION, SO RESET ANGLES.
   }

   // RENDER EVERYTHING IN SCENE

   private void renderWorld() {

      // FIRST TIME: ALLOCATE SPACE FOR TRANSPARENT OBJECTS

      if (tS == null) {
         int n = countT(world);
         tS = new Shape[n];
         tM = new double[n][4][4];
      }

      // RENDER OPAQUE SHAPES

      nt = 0;
      renderT = false;
      renderShape(world, world.matrix, camera);

      // RENDER TRANSPARENT SHAPES

      renderT = true;
      for (int i = 0 ; i < nt ; i++)
         renderShape(tS[i], tM[i]);
   }

   // COUNT HOW MANY TRANSPARENT SHAPES THERE ARE

   private int countT(Shape s) {
      int n = (s.transparency==0 ? 0 : 1);
      if (s.child != null)
         for (int i = 0 ; i < s.child.length && s.child[i] != null ; i++)
            n += countT(s.child[i]);
      return n;
   }

   // RENDER ONE SHAPE FOR THIS FRAME

   private void renderShape(Shape s, double matrix[][], double camera[][]) {

      if (s.child != null) {
         double mat[][] = new double[4][4];
         double cam[][] = new double[4][4];
         double tmp[][] = new double[4][4];

         Matrix.copy(matrix, mat); // NEED LOCAL COPIES, BECAUSE SHAPE AND
         Matrix.copy(camera, cam); // CAMERA MAY MOVE BEFORE CHILD RENDERS

         for (int i = 0 ; i < s.child.length && s.child[i] != null ; i++) {
            Matrix.copy(mat, tmp);
            Matrix.preMultiply(tmp, s.child[i].matrix);
            renderShape(s.child[i], tmp, cam);
         }
      }
      else if (s.faces != null && s.vertices != null) {
         Matrix.postMultiply(matrix, camera);
         renderShape(s, matrix);
      }
   }

   // RENDER ONE SHAPE, TRANSFORMED BY THIS MATRIX

   private int t[][];

   private void renderShape(Shape s, double matrix[][]) {

      if (!renderT && s.transparency != 0) {
         tS[nt] = s;
         Matrix.copy(matrix, tM[nt]);
         nt++;
         return;
      }

      if (t == null || t.length < s.vertices.length)
         t = new int[s.vertices.length][6];

      double r;
      Matrix.copy(matrix, normat);
      for (int j = 0 ; j < 3 ; j++) {
         r = 0;
         for (int i = 0 ; i < 3 ; i++)
            r += normat[i][j]*normat[i][j];
         for (int i = 0 ; i < 3 ; i++)
            normat[i][j] /= r;
      }

      transparency = s.transparency;

      int i = 0;
      int m = s.meshRowSize;
      if (m >= 0)
         s.computeMeshNormals();

      // RECTANGULAR MESH AT COARSE LEVEL OF DETAIL

      if (lod > 1 && m >= 0) {
         int M = m+1, N = s.vertices.length / M;

	 for (int J = 0 ; J < N-1+lod ; J += lod)
	 for (int I = 0 ; I < M-1+lod ; I += lod) {
            int k = Math.min(J,N-1)*M + Math.min(I,M-1);
            transformVertex(matrix, s.vertices[k], k);
            t[k][3] = UNRENDERED;
         }

	 for (int J = 0 ; J <= N-1-lod ; J += lod)
	 for (int I = 0 ; I <= M-1-lod ; I += lod) {
	    int a = J*M+I;
	    int b = J*M+I+lod;
	    int c = (J+lod)*M+I;
	    int d = (J+lod)*M+I+lod;

            if (b%M >= M-lod) b = (b/M+1)*M-1;
            if (d%M >= M-lod) d = (d/M+1)*M-1;

            if (c >= M*(N-lod)) c = M*(N-1) + (c%M);
            if (d >= M*(N-lod)) d = M*(N-1) + (d%M);

            fillTriangle(s, a,b,c);
            fillTriangle(s, b,d,c);
         }
      }

      // ALL OTHER CASES

      else {
         for (int k = 0 ; k < s.vertices.length ; k++) {
            transformVertex(matrix, s.vertices[k], k);
            t[k][3] = UNRENDERED;
         }
         for (int j = 0 ; j < s.faces.length ; j++) {
            int f[] = s.faces[j];
            for (int k = 1 ; k < f.length-1 ; k++)
               fillTriangle(s, f[0], f[k], f[k+1]);
         }
      }
   }

   private void transformVertex(double matrix[][], double v[], int i) {
      xf(matrix, v[0],v[1],v[2],1, ti);

      ti[0] = W/2 + W * ti[0] / (FL - ti[2]) / FOV;
      ti[1] = H/2 - W * ti[1] / (FL - ti[2]) / FOV;
      ti[2] = 1000    * ti[2];

      for (int j = 0 ; j < 3 ; j++)
         t[i][j] = (int)ti[j] << NB;
   }

   private void renderVertex(Shape s, int i){

      if (t[i][3] != UNRENDERED)
         return;

      double v[] = s.vertices[i];
      double nn[] = normal;

      xf(normat, v[3],v[4],v[5],0, nn);
      Vec.normalize(nn);
      for (int j = 0 ; j < 3 ; j++)
         ti[j+3] = nn[j];

      renderVertex(ti, s);

      for (int j = 3 ; j < 6 ; j++)
         t[i][j] = (int)ti[j] << NB;
   }

   // ZBUFFER A TRIANGLE, INTERPOLATING RED,GREEN,BLUE

   private void fillTriangle(Shape s, int iA, int iB, int iC) {

      int A[] = t[iA], B[] = t[iB], C[] = t[iC];

      if (backfacing(A,B,C))
         return;

      renderVertex(s, iA);
      renderVertex(s, iB);
      renderVertex(s, iC);

      int y0 = A[1]<B[1] ? (A[1]<C[1] ? 0 : 2) : (B[1]<C[1] ? 1 : 2);
      int y2 = A[1]>B[1] ? (A[1]>C[1] ? 0 : 2) : (B[1]>C[1] ? 1 : 2);
      int y1 = 3 - (y0 + y2);
      if (y0 == y2)
         return;

      a = y0==0 ? A : y0==1 ? B : C; // FIRST VERTEX IN Y SCAN
      b = y1==0 ? A : y1==1 ? B : C; // MIDDLE VERTEX IN Y SCAN
      d = y2==0 ? A : y2==1 ? B : C; // LAST VERTEX IN Y SCAN

      LEFT   = Math.min(LEFT  , Math.min(Math.min(A[0],B[0]),C[0]) >> NB);
      RIGHT  = Math.max(RIGHT , Math.max(Math.max(A[0],B[0]),C[0]) >> NB);
      TOP    = Math.min(TOP   , Math.min(Math.min(A[1],B[0]),C[1]) >> NB);
      BOTTOM = Math.max(BOTTOM, Math.max(Math.max(A[1],B[0]),C[1]) >> NB);

      double t = (double)(b[1] - a[1]) / (d[1] - a[1]);
      for (int i = 0 ; i < 6 ; i++)
         c[i] = (int)(a[i] + t * (d[i] - a[i])); // SPLIT TOP-TO-BOTTOM EDGE

      // ONLY RENDER FRONT FACING (COUNTER-CLOCKWISE) TRIANGLES

      if ( (y1 == (y0+1) % 3) == c[0] > b[0] ) {
         if (b[0] < c[0]) { fillTrapezoid(a,a,b,c); fillTrapezoid(b,c,d,d); }
         if (b[0] > c[0]) { fillTrapezoid(a,a,c,b); fillTrapezoid(c,b,d,d); }
      }
   }

   private boolean backfacing(int A[], int B[], int C[]) {
      return areaUnder(A,B) + areaUnder(B,C) + areaUnder(C,A) < 0;
   }

   private int areaUnder(int A[], int B[]) {
      return (B[0]-A[0] >> NB) * (B[1]+A[1] >> NB);
   }

/*
THIS IS THE INNER-LOOP RENDERING ROUTINE. IT'S THE COMPUTATIONAL
BOTTLENECK, BECAUSE IT NEEDS TO PROCEED PIXEL BY PIXEL.

BECAUSE JAVA ENFORCES BOUNDS CHECKING ON EVERY ARRAY ACCESS
(WHICH SLOWS THINGS SIGNIFICANTLY), I'VE BROKEN THINGS
OUT HERE INTO INDIVIDUAL VARIABLES WHEREVER I COULD. -KEN
*/

   private void fillTrapezoid(int A[],int B[],int C[],int D[]) {

      int zb[] = zbuffer, px[] = pix; // LOCAL ARRAYS CAN BE FASTER

      int yLo = A[1]>>NB;
      int yHi = C[1]>>NB;
      if (yHi < 0 || yLo >= H)
         return;

      int deltaY = yHi - yLo;
      if (deltaY <= 0)
         return;

      int xL = A[0];
      int zL = A[2];
      int rL = A[3];
      int gL = A[4];
      int bL = A[5];

      int dxL = (C[0] - A[0]) / deltaY;
      int dzL = (C[2] - A[2]) / deltaY;
      int drL = (C[3] - A[3]) / deltaY;
      int dgL = (C[4] - A[4]) / deltaY;
      int dbL = (C[5] - A[5]) / deltaY;

      int xR = B[0];
      int zR = B[2];
      int rR = B[3];
      int gR = B[4];
      int bR = B[5];

      int dxR = (D[0] - B[0]) / deltaY;
      int dzR = (D[2] - B[2]) / deltaY;
      int drR = (D[3] - B[3]) / deltaY;
      int dgR = (D[4] - B[4]) / deltaY;
      int dbR = (D[5] - B[5]) / deltaY;

      int ixL, ixR, deltaX, z, r, g, b, dz=0, dr=0, dg=0, db=0;

      boolean isOpaque = ( transparency <= 0 );
      int opacity = (int)((1-transparency) * (1<<NB));
      int r0,g0,b0, r1,g1,b1, packed;

      if (yLo < 0) {
         xL -= dxL * yLo;
         zL -= dzL * yLo;
         rL -= drL * yLo;
         gL -= dgL * yLo;
         bL -= dbL * yLo;

         xR -= dxR * yLo;
         zR -= dzR * yLo;
         rR -= drR * yLo;
         gR -= dgR * yLo;
         bR -= dbR * yLo;
         yLo = 0;
      }
      yHi = Math.min(yHi, H);

      for (int y = yLo ; y < yHi ; y++) {

         ixL = xL >> NB;
         ixR = xR >> NB;

         deltaX = ixR - ixL;
         z = zL;
         r = rL;
         g = gL;
         b = bL;
         if (deltaX > 0) {
            dz = (zR - zL) / deltaX;
            dr = (rR - rL) / deltaX;
            dg = (gR - gL) / deltaX;
            db = (bR - bL) / deltaX;
         }

         if (ixL < 0) {
            z -= dz * ixL;
            r -= dr * ixL;
            g -= dg * ixL;
            b -= db * ixL;
            ixL = 0;
         }

         ixR = Math.min(ixR, W);

         int i = xy2i(ixL,y);
         for (int ix = ixL ; ix < ixR ; ix++) {
            if (z > zb[i]) {
               zb[i] = z;
               if (isOpaque)
                  px[i] = pack(r>>NB,g>>NB,b>>NB);
               else {
                  packed = px[i];
                  r0 = (packed >> 16) & 255;
                  g0 = (packed >>  8) & 255;
                  b0 = (packed      ) & 255;
                  px[i] = pack(r0 + (opacity*((r>>NB) - r0) >> NB),
                               g0 + (opacity*((g>>NB) - g0) >> NB),
                               b0 + (opacity*((b>>NB) - b0) >> NB));
               }
            }

            z += dz;
            r += dr;
            g += dg;
            b += db;
            i++;
         }

         xL += dxL;
         zL += dzL;
         rL += drL;
         gL += dgL;
         bL += dbL;

         xR += dxR;
         zR += dzR;
         rR += drR;
         gR += dgR;
         bR += dbR;
      }
   }

   // TRANSFORM ONE VERTEX OR NORMAL BY A MATRIX

   private void xf(double m[][],double x,double y,double z,double w,double v[]){
      for (int j = 0 ; j < 3 ; j++)
         v[j] = m[j][0]*x + m[j][1]*y + m[j][2]*z + m[j][3]*w;
   }

   // DO LIGHTING AND SHADING FOR ONE VERTEX OF A SHAPE

   // I WILL BE ABLE TO GET SUBSTANTIAL SPEED-UP IF I CONVERT THIS ENTIRE
   // ROUTINE TO FIXED POINT, AND USE TABLE LOOKUP FOR SPECULAR POWER.

   // I ALSO NEED TO ADD IN EXTENDED LIGHT SOURCES (JUST LOWER THE POWER
   // WHEN DOING SHINY CALCULATION). -KEN

   private void renderVertex(double v[], Shape s) {
      double x=v[3], y=v[4], z=v[5];
      double r = 0, g = 0, b = 0, t, L[];
      double rS = 0, gS = 0, bS = 0;
      double C[] = s.color, G[] = s.glow;
      double red, grn, blu;

      boolean isShiny = (C[3]!=0 || C[4]!=0 || C[5]!=0);
      boolean isGlowing = (G[0]!=0 || G[1]!=0 || G[2]!=0);

      for (int i = 0 ; i < nLights ; i++) {

         L = light[i];
         t = Math.max(0, L[0]*x + L[1]*y + L[2]*z);
         r += L[3] * t;
         g += L[4] * t;
         b += L[5] * t;

         if (isShiny) {
            //t = computeHilite(0,0,1, x,y,z, L);
            t = computeFastHilite(x,y,z, L);
            t = Math.pow(Math.max(0, t), C[6]);
            rS += L[3] * t;
            gS += L[4] * t;
            bS += L[5] * t;
         }
      }

      red = r * C[0];
      grn = g * C[1];
      blu = b * C[2];

      if (isShiny) {
         red += rS * C[3];
         grn += gS * C[4];
         blu += bS * C[5];
      }
      if (isGlowing) {
         red += G[0];
         grn += G[1];
         blu += G[2];
      }

      v[3] = Math.max(0, Math.min(255, 255 * red));
      v[4] = Math.max(0, Math.min(255, 255 * grn));
      v[5] = Math.max(0, Math.min(255, 255 * blu));
   }

   // COMPUTE DIRECTION OF SPECULAR REFLECTION, THEN DOT PRODUCT WITH LIGHT

   private double computeHilite(double x,double y,double z,
                            double nx,double ny,double nz, double L[]) {
      double d = 2 * (x*nx + y*ny + z*nz);
      double rx = d * nx - x;
      double ry = d * ny - y;
      double rz = d * nz - z;
      return L[0]*rx + L[1]*ry + L[2]*rz;
   }

   // FASTER VERSION OF HILITE, WHICH ASSUMES CAMERA IS IN Z DIRECTION

   private double computeFastHilite(double nx,double ny,double nz,double L[]) {
      return 2 * nz * (L[0]*nx + L[1]*ny + L[2]*nz) - L[2];
   }

//--- PRIVATE DATA FIELDS FOR RENDERER

   private double FL = 10;             // FOCAL LENGTH OF VIEW
   private double FOV = 1;             // FIELD OF VIEW
   private Shape world = new Shape();  // THE ROOT OF THE GEOMETRY TREE
   private int W, H;                   // THE RESOLUTION OF THE IMAGE
   private double theta = 0, phi = 0;  // VIEW ROTATION ANGLES
   private int pix[];                  // THE FRAME BUFFER
   private int bgColor = pack(0,0,0);  // BACKGROUND FILL COLOR
   private final int zHuge = 1<<31;    // BIGGEST POSSIBLE ZBUFFER VALUE
   private int TOP=-1,BOTTOM,LEFT,RIGHT; // PIXEL BOUNDS FOR DAMAGED IMAGE
   private int zbuffer[] = null;       // THE ZBUFFER
   private double camera[][] = new double[4][4];  // THE CAMERA MATRIX
   private double camtmp[][] = new double[4][4];  // CAMERA TEMP MATRIX
   private double matrix[][] = new double[4][4]; // TEMP MATRIX
   private int nt = 0;                 // NUM. OF TRANSPARENT SHAPES
   private Shape tS[] = null;          // LIST OF TRANSPARENT SHAPES
   private double tM[][][] = null;     // LIST OF TRANSP SHAPE MATRICES
   private boolean renderT = false;    // IS THIS TRANSP RENDER PASS?
   private double normal[] = new double[3];      // VERTEX NORMAL
   private double ti[] = new double[6];
   private double normat[][] = new double[4][4]; // NORMAL MATRIX XFORM
   private double transparency;        // TRANSPARENCY FOR CURRENT SHAPE
   private final int NB = 14;          // PRECISION FOR FIXED PT PIXEL OPS
   private int a[],b[],c[]=new int[6],d[]; // TEMPS FOR FILLING TRIANGLE
   private int nLights = 0;            // NUM. OF LIGHT SOURCES DEFINED
   private double light[][] = new double [20][6]; // DATA FOR LIGHTS
   private double refl[] = new double[3]; // TEMP TO COMPUTE REFL VECTOR
   private final int UNRENDERED = 1234567; // RENDERING PHASE
}

