#include <stdio.h>
#include <stdlib.h>

typedef struct {
    float x;
    float y;
} Point2D;

int main() {
    FILE *file = fopen("cnc_path.bin", "rb");
    
    unsigned int num_points;
    fread(&num_points, sizeof(unsigned int), 1, file);
    
    Point2D *path = malloc(num_points * sizeof(Point2D));
    fread(path, sizeof(Point2D), num_points, file);
    
    fclose(file);
    
    // Use the path
    for (int i = 0; i < num_points; i++) {
        printf("Point %d: (%.3f, %.3f)\n", i, path[i].x, path[i].y);
    }
    
    free(path);
    return 0;
}