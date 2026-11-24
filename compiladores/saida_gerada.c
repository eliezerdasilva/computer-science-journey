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
  largura = (int)(120.0000);
  altura  = (int)(120.0000);
  if (canvas) gdImageDestroy(canvas);
  canvas = gdImageCreateTrueColor(largura, altura);
  { int bg = cor_gd("#191970");
    gdImageFilledRectangle(canvas, 0,0, largura-1, altura-1, bg); }
  { int bg = cor_gd("#191970");
    gdImageFilledRectangle(canvas, 0,0, largura-1, altura-1, bg); }
  { int _x = (int)(20.0000), _y = (int)(20.0000), _w = (int)(80.0000), _h = (int)(80.0000);
    gdImageFilledRectangle(canvas, _x,_y, _x+_w-1, _y+_h-1, cor_gd("#00FF00")); }
  { int _cx = (int)(60.0000), _cy = (int)(60.0000), _r = (int)(25.0000);
    gdImageFilledEllipse(canvas, _cx,_cy, 2*_r, 2*_r, cor_gd("#FFFF00")); }
  gdImageLine(canvas, (int)(20.0000), (int)(20.0000), (int)(100.0000), (int)(100.0000), cor_gd("#FF0000"));
  if (!canvas) { fprintf(stderr, "Nenhum canvas.\n"); return 1; }
  { FILE *f = fopen("estatico.png", "wb");
    if (!f) { perror("fopen"); return 1; }
    gdImagePng(canvas, f); fclose(f); }
  gdImageDestroy(canvas);
  printf("Imagem salva em estatico.png\n");
  return 0;
}
