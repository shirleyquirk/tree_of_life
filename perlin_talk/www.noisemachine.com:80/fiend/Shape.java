//<pre>
import java.awt.*;

// A VERY SIMPLE 3D RENDERER BUILT IN JAVA 1.0 - KEN PERLIN

public class Shape
{

private String notice = "Copyright 2001 Ken Perlin. All rights reserved.";

   public Shape child[];
   public double[] color = { 1,1,1, 0,0,0,1 };
   public double[][] matrix = new double[4][4];
   public int[][] faces;
   public double[][] vertices;
   public double transparency = 0, glow[] = {0,0,0};
   public int meshRowSize = -1;

   public Shape() {
      Matrix.identity(matrix);
   }

   public Shape add() {
      return add(new Shape());
   }
   public Shape add(Shape s) {
      if (child == null)
         child = new Shape[16];
      else if (child[child.length-1] != null) {
         Shape c[] = child;
         child = new Shape[2*c.length];
         for (int i = 0 ; i < c.length ; i++)
            child[i] = c[i];
      }

      for (int i = 0 ; i < child.length ; i++)
         if (child[i] == null) {
            child[i] = s;
            break;
         }

     s.setColor(color);
     s.setTransparency(transparency);
     s.setGlow(glow);
     return s;
   }

   public Shape setColor(double c[]) {
      for (int i = 0 ; i < c.length ; i++)
         color[i] = c[i];
      return this;
   }

   public Shape setColor(double r, double g, double b) {
      color[0] = r;
      color[1] = g;
      color[2] = b;
      if (child != null)
         for (int i = 0 ; i < child.length && child[i] != null ; i++)
            child[i].setColor(r,g,b);
      return this;
   }

   public Shape setColor(double r, double g, double b,
                         double sr, double sg, double sb, double p) {
      color[0] = r;
      color[1] = g;
      color[2] = b;
      color[3] = sr;
      color[4] = sg;
      color[5] = sb;
      color[6] = p;
      if (child != null)
         for (int i = 0 ; i < child.length && child[i] != null ; i++)
            child[i].setColor(r,g,b,sr,sg,sb,p);
      return this;
   }

   public Shape setTransparency(double t) {
      transparency = t;
      if (child != null)
         for (int i = 0 ; i < child.length && child[i] != null ; i++)
            child[i].setTransparency(t);
      return this;
   }

   public Shape setGlow(double g[]) {
      for (int i = 0 ; i < 3 ; i++)
         glow[i] = g[i];
      return this;
   }

   public Shape setGlow(double r, double g, double b) {
      glow[0] = r;
      glow[1] = g;
      glow[2] = b;
      if (child != null)
         for (int i = 0 ; i < child.length && child[i] != null ; i++)
            child[i].setGlow(r,g,b);
      return this;
   }

   public void setMatrix(double m[][]) {
      Matrix.copy(m, matrix);
   }

   private double[][] copyVertices(double v[][]) {
      double w[][] = new double[v.length][6];
      for (int i = 0 ; i < v.length ; i++)
      for (int j = 0 ; j < 6 ; j++)
         w[i][j] = v[i][j];
      return w;
   }

   private void setVertex(int i,double x , double y , double z ,
                                double nx, double ny, double nz) {
      vertices[i][0] = x;
      vertices[i][1] = y;
      vertices[i][2] = z;
      vertices[i][3] = nx;
      vertices[i][4] = ny;
      vertices[i][5] = nz;
   }

// CUBE

   public Shape cube() {
      faces = cubeFaces;
      vertices = cubeVertices;
      return this;
   }

   private static int[][] cubeFaces = {
      { 0, 1, 2, 3}, { 4, 5, 6, 7},
      { 8, 9,10,11}, {12,13,14,15},
      {16,17,18,19}, {20,21,22,23},
   };

   private static double N=-1, P=1;
   private static double[][] cubeVertices = {

      {N,N,N, N,0,0},{N,N,P, N,0,0},{N,P,P, N,0,0},{N,P,N, N,0,0},
      {P,N,N, P,0,0},{P,P,N, P,0,0},{P,P,P, P,0,0},{P,N,P, P,0,0},

      {N,N,N, 0,N,0},{P,N,N, 0,N,0},{P,N,P, 0,N,0},{N,N,P, 0,N,0},
      {N,P,N, 0,P,0},{N,P,P, 0,P,0},{P,P,P, 0,P,0},{P,P,N, 0,P,0},

      {N,N,N, 0,0,N},{N,P,N, 0,0,N},{P,P,N, 0,0,N},{P,N,N, 0,0,N},
      {N,N,P, 0,0,P},{P,N,P, 0,0,P},{P,P,P, 0,0,P},{N,P,P, 0,0,P},
   };

// BEZELED CUBE

   public Shape bezeledCube(double r) {
      faces = bezeledCubeFaces;
      vertices = copyVertices(bezeledCubeVertices);
      for (int i = 0 ; i < vertices.length ; i++)
      for (int j = 0 ; j < 3 ; j++) {
         if (vertices[i][j] == n) vertices[i][j] = r-1;
         if (vertices[i][j] == p) vertices[i][j] = 1-r;
      }
      return this;
   }

   private static int[][] bezeledCubeFaces = {
      { 0, 1, 2, 3}, { 4, 5, 6, 7},
      { 8, 9,10,11}, {12,13,14,15},
      {16,17,18,19}, {20,21,22,23},

      { 8,11, 1, 0}, {20,23, 2, 1},
      {13,12, 3, 2}, {17,16, 0, 3},

      {16,19, 9, 8}, {11,10,21,20},
      {23,22,14,13}, {12,15,18,17},

      { 4, 7,10, 9}, { 7, 6,22,21},
      { 6, 5,15,14}, { 5, 4,19,18},

      {16, 8, 0}, {11,20, 1}, {23,13, 2}, {12,17, 3},
      { 9,19, 4}, {21,10, 7}, {14,22, 6}, {18,15, 5},
   };

   private static double n=-.9,p=.9;
   private static double[][] bezeledCubeVertices = {

      {N,n,n, N,0,0},{N,n,p, N,0,0},{N,p,p, N,0,0},{N,p,n, N,0,0},
      {P,n,n, P,0,0},{P,p,n, P,0,0},{P,p,p, P,0,0},{P,n,p, P,0,0},

      {n,N,n, 0,N,0},{p,N,n, 0,N,0},{p,N,p, 0,N,0},{n,N,p, 0,N,0},
      {n,P,n, 0,P,0},{n,P,p, 0,P,0},{p,P,p, 0,P,0},{p,P,n, 0,P,0},

      {n,n,N, 0,0,N},{n,p,N, 0,0,N},{p,p,N, 0,0,N},{p,n,N, 0,0,N},
      {n,n,P, 0,0,P},{p,n,P, 0,0,P},{p,p,P, 0,0,P},{n,p,P, 0,0,P},
   };

// TUBE

   private static int[][][] tubeFaces = new int[100][][];
   private static double[][][] tubeVertices = new double[100][][];

   public Shape tube(int k) {
      k = Math.max(3, Math.min(tubeFaces.length-1, k));

      if (tubeFaces[k] == null) {
         tubeFaces[k] = new int[2*k][4];
         tubeVertices[k] = new double[2*k][6];

         faces = tubeFaces[k];
         vertices = tubeVertices[k];
         for (int i = 0 ; i < k ; i++) {
            faces[i][0] = i;
            faces[i][1] = (i+1) % k;
            faces[i][2] = k+((i+1) % k);
            faces[i][3] = k+i;

            double theta = 2 * Math.PI * i / k;
            double c = Math.cos(theta);
            double s = Math.sin(theta);
            setVertex(  i, c, s, -1, c, s, 0);
            setVertex(k+i, c, s,  1, c, s, 0);
         }
      } 

      faces = tubeFaces[k];
      vertices = tubeVertices[k];

      return this;
   }

// DISK

   private static int[][][] diskFaces = new int[100][][];
   private static double[][][] diskVertices = new double[100][][];

   public Shape disk(int k) {

      k = Math.max(3, Math.min(diskFaces.length-1, k));

      if (diskFaces[k] == null) {
         diskFaces[k] = new int[1][k];
         diskVertices[k] = new double[k][6];

         faces = diskFaces[k];
         vertices = diskVertices[k];
         for (int i = 0 ; i < k ; i++) {
            faces[0][i] = i;
            double theta = 2 * Math.PI * i / k;
            setVertex(i, Math.cos(theta),Math.sin(theta),0, 0,0,1);
         }
      } 

      faces = diskFaces[k];
      vertices = diskVertices[k];

      return this;
   }

   private double m[][] = new double[4][4];

// CYLINDER

   public Shape cylinder(int k) {

      add().tube(k);
      add().disk(k);
      add().disk(k);

      Matrix.identity(m);
      Matrix.scale(m, 1,-1,-1);
      Matrix.translate(m, 0,0,1);
      child[1].setMatrix(m);

      Matrix.identity(m);
      Matrix.translate(m, 0,0,1);
      child[2].setMatrix(m);

      return this;
   }

// PILL (TUBE WITH ROUNDED ENDS)

   public Shape pill(int k, double len, double bulge) {
      return pill(k, len, bulge, 1);
   }

// TAPERED PILL (TAPERED TUBE WITH ROUNDED ENDS)

   public Shape pill(int k, double len, double bulge, double taper) {

      add().tube(k, taper);
      add().globe(k,k/2,0,1,0,.5);
      add().globe(k,k/2,0,1,.5,1);

      Matrix.identity(m);
      Matrix.scale(m, 1,1,len);
      child[0].setMatrix(m);

      Matrix.identity(m);
      Matrix.translate(m, 0,0,-len);
      Matrix.scale(m, 1,1,bulge);
      child[1].setMatrix(m);

      Matrix.identity(m);
      Matrix.translate(m, 0,0,len);
      Matrix.scale(m, taper,taper,bulge);
      child[2].setMatrix(m);

      return this;
   }

// BALL

   public Shape ball(int n) {

      for (int i = 0 ; i < 6 ; i++) {
         Shape s = add().newBallFace(n);
         switch (i) {
         case 1: Matrix.rotateX(s.matrix, Math.PI/2); break;
         case 2: Matrix.rotateX(s.matrix, Math.PI  ); break;
         case 3: Matrix.rotateX(s.matrix,-Math.PI/2); break;
         case 4: Matrix.rotateY(s.matrix, Math.PI/2); break;
         case 5: Matrix.rotateY(s.matrix,-Math.PI/2); break;
         }
      }
      return this;
   }

   private Shape newBallFace(int n) {
      newRectangularMesh(n, n);
      int N = 0;
      for (int j = 0 ; j <= n ; j++)
      for (int i = 0 ; i <= n ; i++) {
         double x = Math.tan(Math.PI/4 * (j-n/2) / (n/2));
         double y = Math.tan(Math.PI/4 * (i-n/2) / (n/2));
         double r = Math.sqrt(x*x + y*y + 1);
         x /= r;
         y /= r;
         double z = -1 / r;
         setVertex(N++, x, y, z, x, y, z);
      }
      computedMeshNormals = true;
      return this;
   }

// GLOBE (LONGITUDE/LATITUDE SPHERE)

   public Shape globe(int m,int n) {
      return globe(m, n, 0, 1, 0, 1);
   }

// PARAMETRIC SUBSECTION OF A GLOBE

   public Shape globe(int m,int n,double uLo,double uHi,double vLo,double vHi) {
      newRectangularMesh(m, n);
      int N = 0;
      for (int j = 0 ; j <= n ; j++)
      for (int i = 0 ; i <= m ; i++) {
         double u = uLo + i * (uHi - uLo) / m;
         double v = vLo + j * (vHi - vLo) / n;
         double theta = u * 2 * Math.PI;
         double phi = (v-.5) * Math.PI;
         double x = Math.cos(phi) * Math.cos(theta);
         double y = Math.cos(phi) * Math.sin(theta);
         double z = Math.sin(phi);
         setVertex(N++, x,y,z, x,y,z);
      }
      computedMeshNormals = true;
      return this;
   }

   public Shape wire(int m, int n, double key[][], double r) {
      return wire(m, makePath(n, key), r);
   }

   public Shape wire(int m, double path[][], double r) {
      return extrusion(makeCircle(m, r), path);
   }

   public Shape extrusion(double O[][], double P[][]) {

      int m = O.length-1;
      int n = P.length-1;

      newRectangularMesh(m, n);

      double U[] = new double[3];
      double V[] = new double[3];
      double W[] = new double[3];

      boolean loop = same(P[0],P[n]);

      int N = 0;
      for (int j = 0 ; j <= n ; j++) {
	 for (int k = 0 ; k < 3 ; k++) {
            U[k] = P[j][k+3];
	    W[k] = j == n ? ( loop ? P[1][k]-P[0][k]
                                   : P[n][k]-P[n-1][k] )
                          : P[j+1][k]-P[j][k];
         }
         double radius = Vec.norm(U);
         computeCrossVectors(W, U, V);
         for (int i = 0 ; i <= m ; i++) {
            double x = O[i][0];
            double y = O[i][1];
            double z = O[i][2];
	    for (int k = 0 ; k < 3 ; k++)
	       vertices[N][k] = P[j][k] + radius * (x*U[k] - y*V[k] + z*W[k]);
            N++;
         }
         double ux = U[0],uy = U[1],uz = U[2];
      }
      if (loop)
         for (int i = 0 ; i <= m ; i++)
            for (int k = 0 ; k < 3 ; k++)
               vertices[indx(m,n,i,n)][k] = vertices[indx(m,n,i,0)][k];

      return this;
   }

   public void computeCrossVectors(double W[], double U[], double V[]) {
      Vec.normalize(W);
      Vec.normalize(U);
      Vec.cross(W,U,V);
      Vec.normalize(V);
      Vec.cross(V,W,U);
      Vec.normalize(U);
   }

   public void computeMeshNormals() {
      if (meshRowSize < 0 || computedMeshNormals)
         return;

      int m = meshRowSize, n = vertices.length / (m+1) - 1;

      double nn[] = new double[3];
      double A[] = new double[3], B[] = new double[3];
      boolean loopI = same(vertices[indx(m,n,0,0)],vertices[indx(m,n,m,0)]);
      boolean loopJ = same(vertices[indx(m,n,0,0)],vertices[indx(m,n,0,n)]);
      int N = 0;
      for (int j = 0 ; j <= n ; j++)
      for (int i = 0 ; i <= m ; i++) {
         int i0 = loopI ? (m+i-1)%m : Math.max(0,i-1);
         int i1 = loopI ? (m+i+1)%m : Math.min(m,i+1);
         int j0 = loopJ ? (n+j-1)%n : Math.max(0,j-1);
         int j1 = loopJ ? (n+j+1)%n : Math.min(n,j+1);
         double a[] = vertices[indx(m,n,i0,j0)];
         double b[] = vertices[indx(m,n,i1,j0)];
         double c[] = vertices[indx(m,n,i0,j1)];
         double d[] = vertices[indx(m,n,i1,j1)];
         for (int k = 0 ; k < 3 ; k++) {
            A[k] = d[k] - a[k];
            B[k] = c[k] - b[k];
         }
         Vec.cross(A, B, nn);
         Vec.normalize(nn);
	 for (int k = 0 ; k < 3 ; k++)
            vertices[N][k+3] = nn[k];
         N++;
      }
      computedMeshNormals = true;
   }

   private int indx(int m, int n, int i, int j) {
      return j * (m+1) + i;
   }

   public Shape tube(int m, double taper) {
      double T[] = {-1,1};
      double C[] = {1,taper};
      return latheGen(m, T, C, false);
   }

// LATHE (OBJECT FORMED ON A LATHE)

   public Shape lathe(int m, int n, double Z[], double R[]) {

      double T[] = new double[n+1];
      double C[] = new double[n+1];
      makeCurve(Z, R, T, C);
      return latheGen(m, T, C, true);
   }

   private Shape latheGen(int m, double T[], double C[], boolean round) {
      
      int n = T.length-1;

      newRectangularMesh(m, n);

      for (int i = 0 ; i <= n ; i++)
      for (int j = 0 ; j <= m ; j++) {
         double theta = 2 * Math.PI * j / m;
         double x = Math.cos(theta);
         double y = Math.sin(theta);
         double z = T[i];
         double r = C[i];
         double sign = T[0] < T[n] ? 1 : -1;
         double dr;
         if (round)
            dr = i==0 ? -sign : i==n ? sign : (C[i+1] - C[i-1])/(2*r);
         else
            dr = (C[1]-C[0])/r;
         double nn[] = {r*x,r*y,dr};
         Vec.normalize(nn);
         setVertex(i * (m+1) + j, r*x,r*y,z, nn[0],nn[1],nn[2]);
      }
      computedMeshNormals = true;

      return this;
   }

   private void newRectangularMesh(int m, int n) {

      meshRowSize = m;

      faces = new int[m*n][4];

      for (int k = 0 ; k < n ; k++)
      for (int j = 0 ; j < m ; j++) {
         int f = k *  m    + j;
         int v = k * (m+1) + j;
         faces[f][0] = v;
         faces[f][1] = v + 1;
         faces[f][2] = v + m+1 + 1;
         faces[f][3] = v + m+1;
      }

      vertices = new double[(m+1)*(n+1)][6];

      computedMeshNormals = false;
   }

   public static double[][] makePath(int n, double key[][]) {

      double P[][] = new double[n+1][6];
      int nKeys = key.length-1;

      for (int i = 0 ; i <= n ; i++) {
	 double t = i / (nKeys-.9999);
	 int k = (int)(t * nKeys);
	 double f = t * k - k;
	 for (int j = 0 ; j < 3 ; j++)
	    P[i][j] = hermite(0,1, key[k][  j], key[k+1][  j],
                                   key[k][3+j], key[k+1][3+j], f);
      }
      return P;
   }

   public static double[][] makeCircle(int n, double radius) {
      double P[][] = new double[n+1][6];
      for (int i = 0 ; i <= n ; i++) {
         double theta = 2 * Math.PI * i / n;
         double cos = Math.cos(theta);
         double sin = Math.sin(theta);

         P[i][0] = radius * cos; // LOCATION
         P[i][1] = radius * sin;
         P[i][2] = 0;

         P[i][3] = cos;          // NORMAL DIRECTION
         P[i][4] = sin;
         P[i][5] = 0;
      }
      return P;
   }

   public static void makeCurve(double X[],double Y[], double T[],double C[]) {
      double S[] = new double[X.length]; // SLOPE
      int n = X.length;

      for (int i = 1 ; i < n-1 ; i++)
         S[i] = (Y[i]>=Y[i-1]) == (Y[i]>=Y[i+1])
              ? 0
              : ( (Y[i+1] - Y[i  ]) * (X[i  ] - X[i-1])+
                  (Y[i  ] - Y[i-1]) * (X[i+1] - X[i  ]))
                /((X[i+1] - X[i-1]) * (X[i+1] - X[i-1]));

      S[ 0 ] = 2 * (Y[ 1 ]-Y[ 0 ]) / (X[ 1 ]-X[ 0 ]) - S[ 1 ];
      S[n-1] = 2 * (Y[n-1]-Y[n-2]) / (X[n-1]-X[n-2]) - S[n-2];

      int k = C.length;
      for (int j = 0 ; j < k ; j++) {
         double t = j / (k-.99);
         double x = X[0] + t * (X[n-1] - X[0]);
         int i = 0;
         for ( ; i < n-1 ; i++)
            if (x >= X[i] && x < X[i+1])
               break;
         T[j] = x;
         C[j] = hermite(X[i], X[i+1], Y[i], Y[i+1], S[i], S[i+1], x);
      }
   }

   private static double hermite(double x0,double x1,double y0,double y1,
                          double s0,double s1,double x) {
      double t = (x - x0) / (x1 - x0);
      double s = 1-t;
      return y0 * s*s*(3 - 2*s)
           + s0 * (1-s)*s*s
           - s1 * (1-t)*t*t
           + y1 * t*t*(3 - 2*t);
   }

   private boolean same(double a[], double b[]) {
      return Math.abs(a[0]-b[0])<.01 &&
             Math.abs(a[1]-b[1])<.01 &&
             Math.abs(a[2]-b[2])<.01 ;
   }

   public void addNoise(double freq, double ampl) {
      double v[][] = vertices, x, y, z, s;
      for (int k = 0 ; k < v.length ; k++) {
         x = freq*v[k][0];
         y = freq*v[k][1];
         z = freq*v[k][2];
         v[k][0] += ampl*Noise.noise(x,y,z);
         v[k][1] += ampl*Noise.noise(y,z,x);
         v[k][2] += ampl*Noise.noise(z,x,y);
      }
      computedMeshNormals = false;
   }

   private boolean computedMeshNormals = false;
}

