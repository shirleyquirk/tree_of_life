//<pre>
public class Test2 extends RenderApplet {

   double path[][] = {
      {0,  0,0,  0,-1,0},
      {1,-.5,0,  1, 0,0},
      {1, .5,0, -1, 0,0},
      {0,  0,0,  0,-1,0},
   };

   public void initialize() {

      setBgColor(.5,.5,.7);

      world.add().ball(15).setColor(.5,.5,.5, 1,1,1,20);
      world.add().cylinder(15).setColor(0,0,.5, 1,1,1,20);
      world.add().ball(15).setColor(.5,0,0, 1,1,1,20);

      addLight(1,1,.5, .8,1,1);
      addLight(1,-1,0, 1,.8,1);
      addLight(-1,0,0, 1,1,.8);
   }

   public void animate(double time) {
      push();
         translate(0,-2,0);
         rotateX(-Math.PI/2 + .1*Math.cos(time*5));
         rotateY(.1*Math.cos(time*3.56));
         push();
            scale(1,1,.5);
            transform(world.child[0]);
         pop();
         translate(0,0,2);
         push();
            scale(.2,.2,2);
            transform(world.child[1]);
         pop();
         translate(0,0,2);
         transform(world.child[2]);
      pop();
   }
}

