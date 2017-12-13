//<pre>
public class Fiend extends RenderApplet {

private String notice = "Copyright 2001 Ken Perlin. All rights reserved.";

   double Z[] = { -1.9, -1.6, -.4, .1};
   double R[] = {    0,   .2,  .5,  0};

   Shape podium, torso, legs, neck, head, eyes, arms, hands;

   public void initialize() {

      setBgColor(.2,0,0);

      arms = world.add();
      for (int i = 0 ; i < 4 ; i++)
         arms.add().lathe(5,16,Z,R).setColor(.8,.6,.4);

      hands = arms.add();
      for (int i = 0 ; i < 2 ; i++)
         hands.add().pill(4,1,.5,.5).setColor(.8,.6,.4);
      for (int i = 2 ; i < 14 ; i++)
         hands.add().pill(3,.9,.3,.6).setColor(.8,.6,.4);
      for (int i = 14 ; i < 20 ; i++)
         hands.add().pill(3,.9,.3,.1).setColor(1.2,1.2,0);

      torso = world.add();
      for (int i = 0 ; i < 2 ; i++)
         torso.add().lathe(5,10,Z,R).setColor(.8,.6,.4);

      legs = world.add();
      for (int i = 0 ; i < 4 ; i++)
         legs.add().lathe(5,10,Z,R).setColor(.8,.6,.4);
      for (int i = 4 ; i < 6 ; i++)
         legs.add().pill(8,.7,.3,.6).setColor(.8,.6,.4);

      eyes = world.add();
      for (int i = 0 ; i < 2 ; i++)
         eyes.add().globe(10,10,-.1,.1,0,1).setColor(0,0,0).setGlow(1,0,0);
      for (int i = 2 ; i < 4 ; i++)
         eyes.add().ball(4).setColor(0,0,0);
      for (int i = 4 ; i < 6 ; i++)
         eyes.add().ball(4).setGlow(1,1,1);

      podium = world.add();
      podium.add().cube();
      podium.add().cube();
      podium.add().cube();

      neck = world.add().tube(8).setColor(.8,.6,.4);
      head = world.add().ball(4).setColor(.8,.6,.4);

      addLight(.5,.5,  0,  0.4, .4, .8);
      addLight(-2,-1,-.1,  1.0,  0,  0);
      addLight( 2,-1,-.5,  0.7,  0,  0);

      setFOV(1.3);
      setFL(8);
   }

   private double time=0;
   private double C(double f) { return Math.cos(f*time); }
   private double S(double f) { return Math.sin(f*time); }

   public void animate(double time) {
      this.time = time;

      rotateY(Math.PI);
      translate(0,-1.9,0);
      rotateX(.3);

// PODIUM

      push();
         rotateX(Math.PI/2);
         translate(0,-1.3,1.4);
         scale(.7,.8,1.75);
         transform(podium);

         identity();
         translate(0,0,-.9);
         scale(1,1,.1);
         transform(podium.child[0]);

         identity();
         scale(.8,.6,.95);
         transform(podium.child[1]);

         identity();
         translate(0,0,.9);
         scale(1.1,1.1,.1);
         transform(podium.child[2]);
      pop();

// LEGS

      for (int i = 0 ; i < 2 ; i++) {
         push();
            rotateZ(.01*C(7));
            rotateX(.01*S(9));
            rotateZ(.01*C(9));
            double sgn = i==0?-1:1;
            translate(-sgn*.17,.26,.05);
            rotateY(-sgn*.046);
            push();
               translate(0,-1.98,.07);
               push();
                  translate(0,-1.65,.03);
                  rotateX(-Math.PI/2);
                  scale(sgn*.1,-sgn*.1,-.24);
                  transform(legs.child[4+i]);
               pop();
               rotateX(-Math.PI/2);
               scale(sgn*.45,sgn*.35,.9);
               transform(legs.child[2+i]);
            pop();
            rotateX(-Math.PI/2);
            scale(sgn*.8,sgn*.6,1.3);
            transform(legs.child[i]);
         pop();
      }

// ROTATION AT WAIST

      rotateZ(-.02*C(1.1));
      rotateZ(-.02*C(1.4));
      rotateY(.2*S(1));
      rotateY(.2*S(1.3));

// ARMS

      translate(0, 2,0);
      transform(arms);

      for (int i = 0 ; i < 2 ; i++) {
         double sgn = (i==0 ? -1 : 1);
         push();
            identity();
            translate(1.8*(i-.5),.07*S(3),0);
            rotateX(-1.7);
            rotateY(-sgn * (.5+.5*S(.7))); // SHOULDER
            rotateX(.9+.3*sgn+C(1.2));
            push();
               translate(0,0,-1.7);
               rotateX(2 * (.5+.5*C(4)));  // ELBOW

               // HANDS

               push();
                  translate(0,0,-1.5);
                  rotateZ(sgn * -.2);
                  scale(2,2,2);
                  rotateY(sgn *(-.2*C(1.2)+.6*S(4))); // WRIST
                  translate(0,0,-.15);

                  // FINGERS

                  for (int j = 0 ; j < 3 ; j++) {
                     push();
                        translate(0,.07*j-.07,-.1+(j==1?0:.04));
                        rotateX(j-1);
                        rotateY(sgn * (.4+.6*C(4)));
                        translate(0,0,-.09);
                        push();
                           translate(0,0,-.1);
                           rotateY(sgn * (.4+.6*S(4)));
                           translate(0,0,-.07);
                           push();
                              translate(0,0,-.08);
                              rotateY(sgn * (.3 - .2*C(4)));
                              translate(0,0,-.05);
                              scale(-.014,.014,-.055);
                              transform(hands.child[2+3*i+j+12]);
                           pop();
                           scale(-.02,.02,-.08);
                           transform(hands.child[2+3*i+j+6]);
                        pop();
                        scale(-.03,.03,-.1);
                        transform(hands.child[2+3*i+j]);
                     pop();
                  }
                  translate(0,0,.05);
                  scale(.04,.1,.1);
                  transform(hands.child[i]); // PALM
               pop();

               scale(.38,.38,.825);
               transform(arms.child[2+i]); // FOREARM
            pop();
            scale(.6,.6,1);
            transform(arms.child[i]); // UPPER ARM
         pop();
      }

// TORSO

      push();
         scale(1.07,1,1);
         for (int i = 0 ; i < 2 ; i++) {
            push();
               double sgn = i==0?-1:1;
               translate(-sgn*.31,.25,0);
               rotateX(-Math.PI/2);
               rotateY(-sgn*.1);
               scale(sgn*1.6,sgn*1,1.2);
               transform(torso.child[i]);
            pop();
         }
      pop();

// NECK

      rotateZ(-.15*C(2));
      translate(0,.5,0);

      push();
         translate(0,0,-.02);
         scale(.27,.6,.25);
         rotateX(Math.PI/2);
         transform(neck);
      pop();

// HEAD

      rotateZ(.15*C(2));
      rotateY(-.5*S(.5));
      translate(0,0.6,-.12);

      push();
         rotateX(.4);

         // EYES

         int click = (int)(10*time);
         boolean blink = (click % 43 == 0 || click % 31 == 0);
         for (int i = 0 ; i < 6 ; i++) {
            double sgn = (i%2)==0 ? -1 : 1;
            push();
               if (blink)
                  scale(0,0,0);
               else if (i < 2) {
                  translate(.16*sgn,-.12,-.46);
                  rotateY(-sgn*.1);
                  rotateZ(sgn*.4);
                  scale(-.21,.21,-.03);
                  rotateY(-Math.PI/2);
               }
               else {
                  translate(.25*sgn+(i<4?0:-.03),-.13,i<4?-.48:-.49);
                  scale(i<4?-.06:-.024,i<4?.09:.03,-.01);
               }
               transform(eyes.child[i]);
            pop();
         }
         scale(.5,.65,.55);
         transform(head);
      pop();
   }
}

