//<pre>
public class Test1 extends RenderApplet {

   public void initialize() {

      setBgColor(.5,.5,.7);

      world.add().cube().setTransparency(0);
      world.add().cylinder(20).setColor(.7,.7,.7,1,1,1,10).setTransparency(.7);
      world.add().ball(20).setColor(1,0,0, 1,1,1,20).setTransparency(.7);
      world.add().cube().setTransparency(.9);

      addLight(1,1,.5, .8,1,1);
      addLight(-1,0,0, 1,1,.8);
      addLight(1,-1,0, 1,.8,1);

      scale(2,2,2);
      transform(world.child[3]);
      scale(.55,.55,.55);
      push();
         translate(0,-.5,0);
         scale(.6,1,.1);
         transform(world.child[0]);
      pop();
      translate(0,.5,0);
      push();
         rotateY(Math.PI/2);
         scale(.4,.4,2.5);
         transform(world.child[1]);
      pop();
      transform(world.child[2]);
   }
}

