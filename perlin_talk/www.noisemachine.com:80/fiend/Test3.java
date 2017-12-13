//<pre>
public class Test3 extends RenderApplet {

   // AN ABSTRACT SCULPTURE.  COPYRIGHT KEN PERLIN, 2001.

   public void initialize() {

      int m =  90;        // NUMBER OF STEPS AROUND THE CIRCUMFERENCE
      int n = 600;       // NUMBER OF STEPS ALONG THE KNOT-SHAPED PATH

      // CREATE THE KNOT-SHAPED PATH

      double knotPath[][] = new double[n+1][6];
      for (int j = 0 ; j <= n ; j++) {
         double theta = 4 * Math.PI * j / n; // GO AROUND CIRCLE TWICE
	 double r = .5 + .11 * Math.cos(1.5 * theta);  // WEAVE RADIUS

	 knotPath[j][0] = Math.sin(theta) * r;
	 knotPath[j][1] = Math.sin(1.5 * theta) * .11; // WEAVE HEIGHT
	 knotPath[j][2] = Math.cos(theta) * r;

	 knotPath[j][3] = 0;
	 knotPath[j][4] = 1; // MUST PROVIDE A PATH NORMAL DIRECTION
	 knotPath[j][5] = 0;
      }

      addLight( 1, 1,-1,  .5 ,.4 ,.4 ); // USE MULTI-TINTED SOFT LIGHTING
      addLight( 1,-1, 1,  .4 ,.5 ,.4 );
      addLight(-1, 1, 1,  .4 ,.4 ,.5 );
      addLight(-1,-1, 1,  .25,.2 ,.2 );
      addLight(-1, 1,-1,  .2 ,.25,.2 );
      addLight( 1,-1,-1,  .2 ,.2 ,.25);


      setFOV(.5); // VIEW IN DRAMATIC CLOSEUP: SMALL FIELD OF VIEW
      setFL(5);   //   AND SHORT FOCAL LENGTH

      // EXTRUDE A THICK (radius=.15) ROUND WIRE ALONG THE KNOT PATH

      Shape sculpture = world.add().wire(m, knotPath, .15);

      // RENDER AS SHINY GOLD METAL, AND ADD A LITTLE "MAGICAL" GLOW

      double r=.4,g=.3,b=.12,S=3.3,G=.13;
      sculpture.setColor(r,g,b,S*r,S*g,S*b,10).setGlow(G*r,G*g,G*b);

      sculpture.addNoise(1.7, .12);  // PERTURB VERTICES WITH
      sculpture.addNoise(3.4, .067); // TWO OCTAVES OF NOISE
   }
}

