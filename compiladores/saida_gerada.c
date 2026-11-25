#include <gd.h>
#include <gdfonts.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

static gdImagePtr canvas = NULL;
static int largura = 0, altura = 0;
static double v[256];

static int cor_gd(const char *h) {
    int r=0,g=0,b=0; sscanf(h+1, "%02x%02x%02x", &r,&g,&b);
    return gdImageColorAllocate(canvas, r, g, b);
}

int main(void) {
  largura = (int)(1200.0000);
  altura  = (int)(1200.0000);
  if (canvas) gdImageDestroy(canvas);
  canvas = gdImageCreateTrueColor(largura, altura);
  { int bg = cor_gd("#1A1A2E");
    gdImageFilledRectangle(canvas, 0,0, largura-1, altura-1, bg); }
  { int bg = cor_gd("#1A1A2E");
    gdImageFilledRectangle(canvas, 0,0, largura-1, altura-1, bg); }
  v[0] = (double)(0.0000);
  v[1] = (double)(26.0000);
  v[2] = (double)(26.0000);
  v[3] = (double)(46.0000);
  for (int __r0 = 0; __r0 < (int)(60.0000); __r0++) {
  gdImageLine(canvas, (int)(0.0000), (int)(v[0]), (int)(1199.0000), (int)(v[0]), cor_gd("#000000"));
  v[0] = (double)((v[0] + 20.0000));
  }
  v[4] = (double)(600.0000);
  v[5] = (double)(720.0000);
  v[6] = (double)(90.0000);
  { int _cx = (int)(v[4]), _cy = (int)(v[5]), _r = (int)((v[6] + 40.0000));
    gdImageFilledEllipse(canvas, _cx,_cy, 2*_r, 2*_r, cor_gd("#FFD54F")); }
  { int _cx = (int)(v[4]), _cy = (int)(v[5]), _r = (int)((v[6] + 20.0000));
    gdImageFilledEllipse(canvas, _cx,_cy, 2*_r, 2*_r, cor_gd("#FFB74D")); }
  { int _cx = (int)(v[4]), _cy = (int)(v[5]), _r = (int)(v[6]);
    gdImageFilledEllipse(canvas, _cx,_cy, 2*_r, 2*_r, cor_gd("#FF8A65")); }
  v[7] = (double)(0.0000);
  v[8] = (double)(0.0000);
  for (int __r1 = 0; __r1 < (int)(12.0000); __r1++) {
  gdImageLine(canvas, (int)(v[4]), (int)(v[5]), (int)((v[4] + 200.0000)), (int)(((v[5] - 200.0000) + (v[8] * 35.0000))), cor_gd("#FFB74D"));
  v[8] = (double)((v[8] + 1.0000));
  }
  gdImageLine(canvas, (int)(0.0000), (int)(800.0000), (int)(150.0000), (int)(620.0000), cor_gd("#2D1B4E"));
  gdImageLine(canvas, (int)(150.0000), (int)(620.0000), (int)(320.0000), (int)(800.0000), cor_gd("#2D1B4E"));
  gdImageLine(canvas, (int)(0.0000), (int)(800.0000), (int)(320.0000), (int)(800.0000), cor_gd("#2D1B4E"));
  gdImageLine(canvas, (int)(280.0000), (int)(820.0000), (int)(480.0000), (int)(580.0000), cor_gd("#3D2B5E"));
  gdImageLine(canvas, (int)(480.0000), (int)(580.0000), (int)(700.0000), (int)(820.0000), cor_gd("#3D2B5E"));
  gdImageLine(canvas, (int)(280.0000), (int)(820.0000), (int)(700.0000), (int)(820.0000), cor_gd("#3D2B5E"));
  gdImageLine(canvas, (int)(650.0000), (int)(810.0000), (int)(850.0000), (int)(560.0000), cor_gd("#2D1B4E"));
  gdImageLine(canvas, (int)(850.0000), (int)(560.0000), (int)(1080.0000), (int)(810.0000), cor_gd("#2D1B4E"));
  gdImageLine(canvas, (int)(650.0000), (int)(810.0000), (int)(1080.0000), (int)(810.0000), cor_gd("#2D1B4E"));
  gdImageLine(canvas, (int)(1000.0000), (int)(830.0000), (int)(1200.0000), (int)(640.0000), cor_gd("#3D2B5E"));
  gdImageLine(canvas, (int)(1200.0000), (int)(640.0000), (int)(1200.0000), (int)(830.0000), cor_gd("#3D2B5E"));
  { int _x = (int)(0.0000), _y = (int)(820.0000), _w = (int)(1200.0000), _h = (int)(380.0000);
    gdImageFilledRectangle(canvas, _x,_y, _x+_w-1, _y+_h-1, cor_gd("#1E3A2F")); }
  { int _x = (int)(0.0000), _y = (int)(860.0000), _w = (int)(1200.0000), _h = (int)(340.0000);
    gdImageFilledRectangle(canvas, _x,_y, _x+_w-1, _y+_h-1, cor_gd("#16302A")); }
  gdImageSetPixel(canvas, (int)(120.0000), (int)(80.0000), cor_gd("#FFFFFF"));
  gdImageSetPixel(canvas, (int)(250.0000), (int)(40.0000), cor_gd("#FFFFFF"));
  gdImageSetPixel(canvas, (int)(380.0000), (int)(120.0000), cor_gd("#FFFFFF"));
  gdImageSetPixel(canvas, (int)(520.0000), (int)(60.0000), cor_gd("#FFFFFF"));
  gdImageSetPixel(canvas, (int)(680.0000), (int)(30.0000), cor_gd("#FFFFFF"));
  gdImageSetPixel(canvas, (int)(780.0000), (int)(100.0000), cor_gd("#FFFFFF"));
  gdImageSetPixel(canvas, (int)(900.0000), (int)(50.0000), cor_gd("#FFFFFF"));
  gdImageSetPixel(canvas, (int)(1050.0000), (int)(90.0000), cor_gd("#FFFFFF"));
  gdImageSetPixel(canvas, (int)(1150.0000), (int)(40.0000), cor_gd("#FFFFFF"));
  gdImageSetPixel(canvas, (int)(80.0000), (int)(200.0000), cor_gd("#FFFFFF"));
  gdImageSetPixel(canvas, (int)(300.0000), (int)(220.0000), cor_gd("#FFFFFF"));
  gdImageSetPixel(canvas, (int)(450.0000), (int)(180.0000), cor_gd("#FFFFFF"));
  gdImageSetPixel(canvas, (int)(620.0000), (int)(250.0000), cor_gd("#FFFFFF"));
  gdImageSetPixel(canvas, (int)(820.0000), (int)(200.0000), cor_gd("#FFFFFF"));
  gdImageSetPixel(canvas, (int)(980.0000), (int)(230.0000), cor_gd("#FFFFFF"));
  gdImageSetPixel(canvas, (int)(1120.0000), (int)(180.0000), cor_gd("#FFFFFF"));
  v[9] = (double)(50.0000);
  v[10] = (double)(300.0000);
  for (int __r2 = 0; __r2 < (int)(20.0000); __r2++) {
  gdImageSetPixel(canvas, (int)(v[9]), (int)(v[10]), cor_gd("#E0E0FF"));
  gdImageSetPixel(canvas, (int)((v[9] + 5.0000)), (int)((v[10] + 3.0000)), cor_gd("#FFFFFF"));
  gdImageSetPixel(canvas, (int)((v[9] - 3.0000)), (int)((v[10] + 5.0000)), cor_gd("#C0C0FF"));
  v[9] = (double)((v[9] + 60.0000));
  v[10] = (double)((v[10] + 15.0000));
  }
  { int _x = (int)(40.0000), _y = (int)(620.0000), _w = (int)(100.0000), _h = (int)(200.0000);
    gdImageFilledRectangle(canvas, _x,_y, _x+_w-1, _y+_h-1, cor_gd("#2E2E4E")); }
  { int _x = (int)(40.0000), _y = (int)(620.0000), _w = (int)(100.0000), _h = (int)(10.0000);
    gdImageFilledRectangle(canvas, _x,_y, _x+_w-1, _y+_h-1, cor_gd("#4E4E6E")); }
  v[11] = (double)(55.0000);
  v[12] = (double)(640.0000);
  for (int __r3 = 0; __r3 < (int)(4.0000); __r3++) {
  for (int __r4 = 0; __r4 < (int)(3.0000); __r4++) {
  { int _x = (int)(v[11]), _y = (int)(v[12]), _w = (int)(12.0000), _h = (int)(18.0000);
    gdImageFilledRectangle(canvas, _x,_y, _x+_w-1, _y+_h-1, cor_gd("#FFD54F")); }
  v[11] = (double)((v[11] + 25.0000));
  }
  v[11] = (double)(55.0000);
  v[12] = (double)((v[12] + 35.0000));
  }
  { int _x = (int)(160.0000), _y = (int)(580.0000), _w = (int)(120.0000), _h = (int)(240.0000);
    gdImageFilledRectangle(canvas, _x,_y, _x+_w-1, _y+_h-1, cor_gd("#3E2E5E")); }
  { int _x = (int)(160.0000), _y = (int)(580.0000), _w = (int)(120.0000), _h = (int)(10.0000);
    gdImageFilledRectangle(canvas, _x,_y, _x+_w-1, _y+_h-1, cor_gd("#5E4E7E")); }
  v[13] = (double)(175.0000);
  v[14] = (double)(600.0000);
  for (int __r5 = 0; __r5 < (int)(5.0000); __r5++) {
  for (int __r6 = 0; __r6 < (int)(4.0000); __r6++) {
  { int _x = (int)(v[13]), _y = (int)(v[14]), _w = (int)(14.0000), _h = (int)(20.0000);
    gdImageFilledRectangle(canvas, _x,_y, _x+_w-1, _y+_h-1, cor_gd("#FFE082")); }
  v[13] = (double)((v[13] + 26.0000));
  }
  v[13] = (double)(175.0000);
  v[14] = (double)((v[14] + 42.0000));
  }
  { int _x = (int)(300.0000), _y = (int)(500.0000), _w = (int)(110.0000), _h = (int)(320.0000);
    gdImageFilledRectangle(canvas, _x,_y, _x+_w-1, _y+_h-1, cor_gd("#2E2E5E")); }
  { int _x = (int)(300.0000), _y = (int)(500.0000), _w = (int)(110.0000), _h = (int)(10.0000);
    gdImageFilledRectangle(canvas, _x,_y, _x+_w-1, _y+_h-1, cor_gd("#4E4E7E")); }
  v[15] = (double)(315.0000);
  v[16] = (double)(520.0000);
  for (int __r7 = 0; __r7 < (int)(6.0000); __r7++) {
  for (int __r8 = 0; __r8 < (int)(3.0000); __r8++) {
  { int _x = (int)(v[15]), _y = (int)(v[16]), _w = (int)(16.0000), _h = (int)(22.0000);
    gdImageFilledRectangle(canvas, _x,_y, _x+_w-1, _y+_h-1, cor_gd("#FFCC80")); }
  v[15] = (double)((v[15] + 28.0000));
  }
  v[15] = (double)(315.0000);
  v[16] = (double)((v[16] + 48.0000));
  }
  { int _x = (int)(430.0000), _y = (int)(650.0000), _w = (int)(90.0000), _h = (int)(170.0000);
    gdImageFilledRectangle(canvas, _x,_y, _x+_w-1, _y+_h-1, cor_gd("#3E2E4E")); }
  { int _x = (int)(430.0000), _y = (int)(650.0000), _w = (int)(90.0000), _h = (int)(8.0000);
    gdImageFilledRectangle(canvas, _x,_y, _x+_w-1, _y+_h-1, cor_gd("#5E4E6E")); }
  v[17] = (double)(445.0000);
  v[18] = (double)(670.0000);
  for (int __r9 = 0; __r9 < (int)(3.0000); __r9++) {
  for (int __r10 = 0; __r10 < (int)(3.0000); __r10++) {
  { int _x = (int)(v[17]), _y = (int)(v[18]), _w = (int)(12.0000), _h = (int)(16.0000);
    gdImageFilledRectangle(canvas, _x,_y, _x+_w-1, _y+_h-1, cor_gd("#FFD54F")); }
  v[17] = (double)((v[17] + 22.0000));
  }
  v[17] = (double)(445.0000);
  v[18] = (double)((v[18] + 40.0000));
  }
  { int _x = (int)(540.0000), _y = (int)(590.0000), _w = (int)(100.0000), _h = (int)(230.0000);
    gdImageFilledRectangle(canvas, _x,_y, _x+_w-1, _y+_h-1, cor_gd("#2E3E5E")); }
  { int _x = (int)(540.0000), _y = (int)(590.0000), _w = (int)(100.0000), _h = (int)(8.0000);
    gdImageFilledRectangle(canvas, _x,_y, _x+_w-1, _y+_h-1, cor_gd("#4E5E7E")); }
  v[19] = (double)(555.0000);
  v[20] = (double)(610.0000);
  for (int __r11 = 0; __r11 < (int)(5.0000); __r11++) {
  for (int __r12 = 0; __r12 < (int)(3.0000); __r12++) {
  { int _x = (int)(v[19]), _y = (int)(v[20]), _w = (int)(14.0000), _h = (int)(20.0000);
    gdImageFilledRectangle(canvas, _x,_y, _x+_w-1, _y+_h-1, cor_gd("#FFE082")); }
  v[19] = (double)((v[19] + 24.0000));
  }
  v[19] = (double)(555.0000);
  v[20] = (double)((v[20] + 42.0000));
  }
  { int _x = (int)(660.0000), _y = (int)(470.0000), _w = (int)(130.0000), _h = (int)(350.0000);
    gdImageFilledRectangle(canvas, _x,_y, _x+_w-1, _y+_h-1, cor_gd("#3E2E6E")); }
  { int _x = (int)(660.0000), _y = (int)(470.0000), _w = (int)(130.0000), _h = (int)(12.0000);
    gdImageFilledRectangle(canvas, _x,_y, _x+_w-1, _y+_h-1, cor_gd("#5E4E8E")); }
  v[21] = (double)(675.0000);
  v[22] = (double)(490.0000);
  for (int __r13 = 0; __r13 < (int)(7.0000); __r13++) {
  for (int __r14 = 0; __r14 < (int)(4.0000); __r14++) {
  { int _x = (int)(v[21]), _y = (int)(v[22]), _w = (int)(16.0000), _h = (int)(22.0000);
    gdImageFilledRectangle(canvas, _x,_y, _x+_w-1, _y+_h-1, cor_gd("#FFCC80")); }
  v[21] = (double)((v[21] + 28.0000));
  }
  v[21] = (double)(675.0000);
  v[22] = (double)((v[22] + 46.0000));
  }
  { int _x = (int)(810.0000), _y = (int)(620.0000), _w = (int)(100.0000), _h = (int)(200.0000);
    gdImageFilledRectangle(canvas, _x,_y, _x+_w-1, _y+_h-1, cor_gd("#2E2E4E")); }
  { int _x = (int)(810.0000), _y = (int)(620.0000), _w = (int)(100.0000), _h = (int)(10.0000);
    gdImageFilledRectangle(canvas, _x,_y, _x+_w-1, _y+_h-1, cor_gd("#4E4E6E")); }
  v[23] = (double)(825.0000);
  v[24] = (double)(640.0000);
  for (int __r15 = 0; __r15 < (int)(4.0000); __r15++) {
  for (int __r16 = 0; __r16 < (int)(3.0000); __r16++) {
  { int _x = (int)(v[23]), _y = (int)(v[24]), _w = (int)(14.0000), _h = (int)(18.0000);
    gdImageFilledRectangle(canvas, _x,_y, _x+_w-1, _y+_h-1, cor_gd("#FFD54F")); }
  v[23] = (double)((v[23] + 26.0000));
  }
  v[23] = (double)(825.0000);
  v[24] = (double)((v[24] + 38.0000));
  }
  { int _x = (int)(930.0000), _y = (int)(450.0000), _w = (int)(120.0000), _h = (int)(370.0000);
    gdImageFilledRectangle(canvas, _x,_y, _x+_w-1, _y+_h-1, cor_gd("#2E3E5E")); }
  { int _x = (int)(930.0000), _y = (int)(450.0000), _w = (int)(120.0000), _h = (int)(10.0000);
    gdImageFilledRectangle(canvas, _x,_y, _x+_w-1, _y+_h-1, cor_gd("#4E5E7E")); }
  { int _x = (int)(955.0000), _y = (int)(420.0000), _w = (int)(70.0000), _h = (int)(30.0000);
    gdImageFilledRectangle(canvas, _x,_y, _x+_w-1, _y+_h-1, cor_gd("#3E4E6E")); }
  v[25] = (double)(945.0000);
  v[26] = (double)(470.0000);
  for (int __r17 = 0; __r17 < (int)(8.0000); __r17++) {
  for (int __r18 = 0; __r18 < (int)(3.0000); __r18++) {
  { int _x = (int)(v[25]), _y = (int)(v[26]), _w = (int)(14.0000), _h = (int)(20.0000);
    gdImageFilledRectangle(canvas, _x,_y, _x+_w-1, _y+_h-1, cor_gd("#FFE082")); }
  v[25] = (double)((v[25] + 30.0000));
  }
  v[25] = (double)(945.0000);
  v[26] = (double)((v[26] + 44.0000));
  }
  { int _x = (int)(1070.0000), _y = (int)(600.0000), _w = (int)(90.0000), _h = (int)(220.0000);
    gdImageFilledRectangle(canvas, _x,_y, _x+_w-1, _y+_h-1, cor_gd("#3E2E5E")); }
  { int _x = (int)(1070.0000), _y = (int)(600.0000), _w = (int)(90.0000), _h = (int)(10.0000);
    gdImageFilledRectangle(canvas, _x,_y, _x+_w-1, _y+_h-1, cor_gd("#5E4E7E")); }
  v[27] = (double)(1085.0000);
  v[28] = (double)(620.0000);
  for (int __r19 = 0; __r19 < (int)(5.0000); __r19++) {
  for (int __r20 = 0; __r20 < (int)(3.0000); __r20++) {
  { int _x = (int)(v[27]), _y = (int)(v[28]), _w = (int)(12.0000), _h = (int)(18.0000);
    gdImageFilledRectangle(canvas, _x,_y, _x+_w-1, _y+_h-1, cor_gd("#FFD54F")); }
  v[27] = (double)((v[27] + 22.0000));
  }
  v[27] = (double)(1085.0000);
  v[28] = (double)((v[28] + 40.0000));
  }
  { int _x = (int)(0.0000), _y = (int)(780.0000), _w = (int)(140.0000), _h = (int)(80.0000);
    gdImageFilledRectangle(canvas, _x,_y, _x+_w-1, _y+_h-1, cor_gd("#1E1E3E")); }
  { int _x = (int)(220.0000), _y = (int)(760.0000), _w = (int)(130.0000), _h = (int)(100.0000);
    gdImageFilledRectangle(canvas, _x,_y, _x+_w-1, _y+_h-1, cor_gd("#1E1E3E")); }
  { int _x = (int)(420.0000), _y = (int)(790.0000), _w = (int)(160.0000), _h = (int)(70.0000);
    gdImageFilledRectangle(canvas, _x,_y, _x+_w-1, _y+_h-1, cor_gd("#1E1E3E")); }
  { int _x = (int)(640.0000), _y = (int)(770.0000), _w = (int)(140.0000), _h = (int)(90.0000);
    gdImageFilledRectangle(canvas, _x,_y, _x+_w-1, _y+_h-1, cor_gd("#1E1E3E")); }
  { int _x = (int)(850.0000), _y = (int)(780.0000), _w = (int)(150.0000), _h = (int)(80.0000);
    gdImageFilledRectangle(canvas, _x,_y, _x+_w-1, _y+_h-1, cor_gd("#1E1E3E")); }
  { int _x = (int)(1050.0000), _y = (int)(760.0000), _w = (int)(150.0000), _h = (int)(100.0000);
    gdImageFilledRectangle(canvas, _x,_y, _x+_w-1, _y+_h-1, cor_gd("#1E1E3E")); }
  v[29] = (double)(20.0000);
  for (int __r21 = 0; __r21 < (int)(5.0000); __r21++) {
  { int _x = (int)(v[29]), _y = (int)(800.0000), _w = (int)(10.0000), _h = (int)(12.0000);
    gdImageFilledRectangle(canvas, _x,_y, _x+_w-1, _y+_h-1, cor_gd("#FFD54F")); }
  { int _x = (int)((v[29] + 25.0000)), _y = (int)(800.0000), _w = (int)(10.0000), _h = (int)(12.0000);
    gdImageFilledRectangle(canvas, _x,_y, _x+_w-1, _y+_h-1, cor_gd("#FFE082")); }
  { int _x = (int)((v[29] + 50.0000)), _y = (int)(800.0000), _w = (int)(10.0000), _h = (int)(12.0000);
    gdImageFilledRectangle(canvas, _x,_y, _x+_w-1, _y+_h-1, cor_gd("#FFD54F")); }
  v[29] = (double)((v[29] + 90.0000));
  }
  v[30] = (double)(240.0000);
  for (int __r22 = 0; __r22 < (int)(5.0000); __r22++) {
  { int _x = (int)(v[30]), _y = (int)(790.0000), _w = (int)(10.0000), _h = (int)(12.0000);
    gdImageFilledRectangle(canvas, _x,_y, _x+_w-1, _y+_h-1, cor_gd("#FFE082")); }
  { int _x = (int)((v[30] + 25.0000)), _y = (int)(790.0000), _w = (int)(10.0000), _h = (int)(12.0000);
    gdImageFilledRectangle(canvas, _x,_y, _x+_w-1, _y+_h-1, cor_gd("#FFD54F")); }
  { int _x = (int)((v[30] + 50.0000)), _y = (int)(790.0000), _w = (int)(10.0000), _h = (int)(12.0000);
    gdImageFilledRectangle(canvas, _x,_y, _x+_w-1, _y+_h-1, cor_gd("#FFE082")); }
  v[30] = (double)((v[30] + 80.0000));
  }
  { int _x = (int)(150.0000), _y = (int)(940.0000), _w = (int)(12.0000), _h = (int)(60.0000);
    gdImageFilledRectangle(canvas, _x,_y, _x+_w-1, _y+_h-1, cor_gd("#3E2A1E")); }
  { int _cx = (int)(156.0000), _cy = (int)(920.0000), _r = (int)(45.0000);
    gdImageFilledEllipse(canvas, _cx,_cy, 2*_r, 2*_r, cor_gd("#2E7D32")); }
  { int _cx = (int)(130.0000), _cy = (int)(930.0000), _r = (int)(35.0000);
    gdImageFilledEllipse(canvas, _cx,_cy, 2*_r, 2*_r, cor_gd("#388E3C")); }
  { int _cx = (int)(180.0000), _cy = (int)(930.0000), _r = (int)(35.0000);
    gdImageFilledEllipse(canvas, _cx,_cy, 2*_r, 2*_r, cor_gd("#388E3C")); }
  { int _cx = (int)(156.0000), _cy = (int)(905.0000), _r = (int)(30.0000);
    gdImageFilledEllipse(canvas, _cx,_cy, 2*_r, 2*_r, cor_gd("#43A047")); }
  { int _x = (int)(380.0000), _y = (int)(950.0000), _w = (int)(12.0000), _h = (int)(50.0000);
    gdImageFilledRectangle(canvas, _x,_y, _x+_w-1, _y+_h-1, cor_gd("#3E2A1E")); }
  { int _cx = (int)(386.0000), _cy = (int)(930.0000), _r = (int)(40.0000);
    gdImageFilledEllipse(canvas, _cx,_cy, 2*_r, 2*_r, cor_gd("#2E7D32")); }
  { int _cx = (int)(360.0000), _cy = (int)(940.0000), _r = (int)(32.0000);
    gdImageFilledEllipse(canvas, _cx,_cy, 2*_r, 2*_r, cor_gd("#388E3C")); }
  { int _cx = (int)(410.0000), _cy = (int)(940.0000), _r = (int)(32.0000);
    gdImageFilledEllipse(canvas, _cx,_cy, 2*_r, 2*_r, cor_gd("#388E3C")); }
  { int _cx = (int)(386.0000), _cy = (int)(915.0000), _r = (int)(28.0000);
    gdImageFilledEllipse(canvas, _cx,_cy, 2*_r, 2*_r, cor_gd("#43A047")); }
  { int _x = (int)(780.0000), _y = (int)(945.0000), _w = (int)(12.0000), _h = (int)(55.0000);
    gdImageFilledRectangle(canvas, _x,_y, _x+_w-1, _y+_h-1, cor_gd("#3E2A1E")); }
  { int _cx = (int)(786.0000), _cy = (int)(925.0000), _r = (int)(42.0000);
    gdImageFilledEllipse(canvas, _cx,_cy, 2*_r, 2*_r, cor_gd("#2E7D32")); }
  { int _cx = (int)(760.0000), _cy = (int)(935.0000), _r = (int)(34.0000);
    gdImageFilledEllipse(canvas, _cx,_cy, 2*_r, 2*_r, cor_gd("#388E3C")); }
  { int _cx = (int)(812.0000), _cy = (int)(935.0000), _r = (int)(34.0000);
    gdImageFilledEllipse(canvas, _cx,_cy, 2*_r, 2*_r, cor_gd("#388E3C")); }
  { int _cx = (int)(786.0000), _cy = (int)(910.0000), _r = (int)(30.0000);
    gdImageFilledEllipse(canvas, _cx,_cy, 2*_r, 2*_r, cor_gd("#43A047")); }
  { int _x = (int)(1050.0000), _y = (int)(950.0000), _w = (int)(12.0000), _h = (int)(50.0000);
    gdImageFilledRectangle(canvas, _x,_y, _x+_w-1, _y+_h-1, cor_gd("#3E2A1E")); }
  { int _cx = (int)(1056.0000), _cy = (int)(930.0000), _r = (int)(40.0000);
    gdImageFilledEllipse(canvas, _cx,_cy, 2*_r, 2*_r, cor_gd("#2E7D32")); }
  { int _cx = (int)(1030.0000), _cy = (int)(940.0000), _r = (int)(32.0000);
    gdImageFilledEllipse(canvas, _cx,_cy, 2*_r, 2*_r, cor_gd("#388E3C")); }
  { int _cx = (int)(1082.0000), _cy = (int)(940.0000), _r = (int)(32.0000);
    gdImageFilledEllipse(canvas, _cx,_cy, 2*_r, 2*_r, cor_gd("#388E3C")); }
  { int _cx = (int)(1056.0000), _cy = (int)(915.0000), _r = (int)(28.0000);
    gdImageFilledEllipse(canvas, _cx,_cy, 2*_r, 2*_r, cor_gd("#43A047")); }
  { int _x = (int)(250.0000), _y = (int)(850.0000), _w = (int)(6.0000), _h = (int)(120.0000);
    gdImageFilledRectangle(canvas, _x,_y, _x+_w-1, _y+_h-1, cor_gd("#1A1A1A")); }
  { int _x = (int)(240.0000), _y = (int)(850.0000), _w = (int)(26.0000), _h = (int)(8.0000);
    gdImageFilledRectangle(canvas, _x,_y, _x+_w-1, _y+_h-1, cor_gd("#1A1A1A")); }
  { int _cx = (int)(253.0000), _cy = (int)(845.0000), _r = (int)(12.0000);
    gdImageFilledEllipse(canvas, _cx,_cy, 2*_r, 2*_r, cor_gd("#FFEB3B")); }
  { int _x = (int)(550.0000), _y = (int)(850.0000), _w = (int)(6.0000), _h = (int)(120.0000);
    gdImageFilledRectangle(canvas, _x,_y, _x+_w-1, _y+_h-1, cor_gd("#1A1A1A")); }
  { int _x = (int)(540.0000), _y = (int)(850.0000), _w = (int)(26.0000), _h = (int)(8.0000);
    gdImageFilledRectangle(canvas, _x,_y, _x+_w-1, _y+_h-1, cor_gd("#1A1A1A")); }
  { int _cx = (int)(553.0000), _cy = (int)(845.0000), _r = (int)(12.0000);
    gdImageFilledEllipse(canvas, _cx,_cy, 2*_r, 2*_r, cor_gd("#FFEB3B")); }
  { int _x = (int)(850.0000), _y = (int)(850.0000), _w = (int)(6.0000), _h = (int)(120.0000);
    gdImageFilledRectangle(canvas, _x,_y, _x+_w-1, _y+_h-1, cor_gd("#1A1A1A")); }
  { int _x = (int)(840.0000), _y = (int)(850.0000), _w = (int)(26.0000), _h = (int)(8.0000);
    gdImageFilledRectangle(canvas, _x,_y, _x+_w-1, _y+_h-1, cor_gd("#1A1A1A")); }
  { int _cx = (int)(853.0000), _cy = (int)(845.0000), _r = (int)(12.0000);
    gdImageFilledEllipse(canvas, _cx,_cy, 2*_r, 2*_r, cor_gd("#FFEB3B")); }
  { int _x = (int)(1150.0000), _y = (int)(850.0000), _w = (int)(6.0000), _h = (int)(120.0000);
    gdImageFilledRectangle(canvas, _x,_y, _x+_w-1, _y+_h-1, cor_gd("#1A1A1A")); }
  { int _x = (int)(1140.0000), _y = (int)(850.0000), _w = (int)(26.0000), _h = (int)(8.0000);
    gdImageFilledRectangle(canvas, _x,_y, _x+_w-1, _y+_h-1, cor_gd("#1A1A1A")); }
  { int _cx = (int)(1153.0000), _cy = (int)(845.0000), _r = (int)(12.0000);
    gdImageFilledEllipse(canvas, _cx,_cy, 2*_r, 2*_r, cor_gd("#FFEB3B")); }
  { int _x = (int)(0.0000), _y = (int)(1000.0000), _w = (int)(1200.0000), _h = (int)(200.0000);
    gdImageFilledRectangle(canvas, _x,_y, _x+_w-1, _y+_h-1, cor_gd("#1A1A1A")); }
  v[31] = (double)(0.0000);
  for (int __r23 = 0; __r23 < (int)(20.0000); __r23++) {
  { int _x = (int)(v[31]), _y = (int)(1095.0000), _w = (int)(40.0000), _h = (int)(10.0000);
    gdImageFilledRectangle(canvas, _x,_y, _x+_w-1, _y+_h-1, cor_gd("#FFEB3B")); }
  v[31] = (double)((v[31] + 60.0000));
  }
  { int _cx = (int)(1000.0000), _cy = (int)(150.0000), _r = (int)(50.0000);
    gdImageFilledEllipse(canvas, _cx,_cy, 2*_r, 2*_r, cor_gd("#E8E8D0")); }
  { int _cx = (int)(1025.0000), _cy = (int)(140.0000), _r = (int)(45.0000);
    gdImageFilledEllipse(canvas, _cx,_cy, 2*_r, 2*_r, cor_gd("#1A1A2E")); }
  gdImageLine(canvas, (int)(300.0000), (int)(150.0000), (int)(340.0000), (int)(200.0000), cor_gd("#FFFFFF"));
  gdImageSetPixel(canvas, (int)(340.0000), (int)(200.0000), cor_gd("#FFFFFF"));
  gdImageSetPixel(canvas, (int)(345.0000), (int)(205.0000), cor_gd("#E0E0FF"));
  gdImageLine(canvas, (int)(700.0000), (int)(100.0000), (int)(730.0000), (int)(140.0000), cor_gd("#FFFFFF"));
  gdImageSetPixel(canvas, (int)(730.0000), (int)(140.0000), cor_gd("#FFFFFF"));
  gdImageSetPixel(canvas, (int)(735.0000), (int)(145.0000), cor_gd("#E0E0FF"));
  gdImageLine(canvas, (int)(400.0000), (int)(300.0000), (int)(420.0000), (int)(290.0000), cor_gd("#000000"));
  gdImageLine(canvas, (int)(420.0000), (int)(290.0000), (int)(440.0000), (int)(300.0000), cor_gd("#000000"));
  gdImageLine(canvas, (int)(500.0000), (int)(350.0000), (int)(515.0000), (int)(342.0000), cor_gd("#000000"));
  gdImageLine(canvas, (int)(515.0000), (int)(342.0000), (int)(530.0000), (int)(350.0000), cor_gd("#000000"));
  gdImageLine(canvas, (int)(620.0000), (int)(280.0000), (int)(635.0000), (int)(272.0000), cor_gd("#000000"));
  gdImageLine(canvas, (int)(635.0000), (int)(272.0000), (int)(650.0000), (int)(280.0000), cor_gd("#000000"));
  gdImageString(canvas, gdFontSmall, (int)(500.0000), (int)(1150.0000), (unsigned char*)"PIXEL CITY", cor_gd("#FFD54F"));
  gdImageString(canvas, gdFontSmall, (int)(580.0000), (int)(1175.0000), (unsigned char*)"2024", cor_gd("#FFE082"));
  { int _x = (int)(700.0000), _y = (int)(500.0000), _w = (int)(16.0000), _h = (int)(22.0000);
    gdImageFilledRectangle(canvas, _x,_y, _x+_w-1, _y+_h-1, cor_gd("#FFFFFF")); }
  { int _x = (int)(700.0000), _y = (int)(500.0000), _w = (int)(16.0000), _h = (int)(22.0000);
    gdImageFilledRectangle(canvas, _x,_y, _x+_w-1, _y+_h-1, cor_gd("#FFCC80")); }
  v[32] = (double)(600.0000);
  v[32] = (double)(620.0000);
  if (!canvas) { fprintf(stderr, "Nenhum canvas.\n"); return 1; }
  { FILE *f = fopen("pixel_city.png", "wb");
    if (!f) { perror("fopen"); return 1; }
    gdImagePng(canvas, f); fclose(f); }
  gdImageDestroy(canvas);
  printf("Imagem salva em pixel_city.png\n");
  system("xdg-open pixel_city.png &");
  return 0;
}
