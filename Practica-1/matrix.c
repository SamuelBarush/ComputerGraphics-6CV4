#include <math.h>
#include "matrix.h"

// Devuelve una matriz identidad 4x4
mat4_t mat4_identity(void) {
    mat4_t result = {0};
    result.m[0][0] = 1.0f;
    result.m[1][0] = 0.0f;
    result.m[2][0] = 0.0f;
    result.m[3][0] = 0.0f;

    result.m[0][1] = 0.0f;
    result.m[1][1] = 1.0f;
    result.m[2][1] = 0.0f;
    result.m[3][1] = 0.0f;

    result.m[0][2] = 0.0f;
    result.m[1][2] = 0.0f;
    result.m[2][2] = 1.0f;
    result.m[3][2] = 0.0f;

    result.m[0][3] = 0.0f;
    result.m[1][3] = 0.0f;
    result.m[2][3] = 0.0f;
    result.m[3][3] = 1.0f;
    return result;
}

// Devuelve una matriz de escalado
mat4_t mat4_make_scale(float sx, float sy, float sz) {
    mat4_t result = mat4_identity();
    result.m[0][0] = sx;
    result.m[1][1] = sy;
    result.m[2][2] = sz;
    return result;
}

// Devuelve una matriz de traslación
mat4_t mat4_make_translation(float tx, float ty, float tz) {
    mat4_t result = mat4_identity();
    result.m[3][0] = tx;
    result.m[3][1] = ty;
    result.m[3][2] = tz;
    return result;
}

// Devuelve una matriz de rotación en el eje X
mat4_t mat4_make_rotation_x(float angle) {
    mat4_t result = mat4_identity();
    float cos_theta = cosf(angle);
    float sin_theta = sinf(angle);

    result.m[1][1] = cos_theta;
    result.m[1][2] = -sin_theta;
    result.m[2][1] = sin_theta;
    result.m[2][2] = cos_theta;

    return result;
}

// Devuelve una matriz de rotación en el eje Y
mat4_t mat4_make_rotation_y(float angle) {
    mat4_t result = mat4_identity();
    float cos_theta = cosf(angle);
    float sin_theta = sinf(angle);

    result.m[0][0] = cos_theta;
    result.m[0][2] = sin_theta;
    result.m[2][0] = -sin_theta;
    result.m[2][2] = cos_theta;

    return result;
}

// Devuelve una matriz de rotación en el eje Z
mat4_t mat4_make_rotation_z(float angle) {
    mat4_t result = mat4_identity();
    float cos_theta = cosf(angle);
    float sin_theta = sinf(angle);

    result.m[0][0] = cos_theta;
    result.m[0][1] = -sin_theta;
    result.m[1][0] = sin_theta;
    result.m[1][1] = cos_theta;

    return result;
}

// Multiplica una matriz 4x4 por un vector 4D
vec4_t mat4_mul_vec4(mat4_t m, vec4_t v) {
    vec4_t result;

    result.x = m.m[0][0] * v.x + m.m[1][0] * v.y + m.m[2][0] * v.z + m.m[3][0] * v.w;
    result.y = m.m[0][1] * v.x + m.m[1][1] * v.y + m.m[2][1] * v.z + m.m[3][1] * v.w;
    result.z = m.m[0][2] * v.x + m.m[1][2] * v.y + m.m[2][2] * v.z + m.m[3][2] * v.w;
    result.w = m.m[0][3] * v.x + m.m[1][3] * v.y + m.m[2][3] * v.z + m.m[3][3] * v.w;

    return result;
}

// Multiplica dos matrices 4x4
mat4_t mat4_mul_mat4(mat4_t a, mat4_t b) {
    mat4_t result = {0};

    for (int i = 0; i < 4; i++) {
        for (int j = 0; j < 4; j++) {
            result.m[i][j] = a.m[i][0] * b.m[0][j] +
                             a.m[i][1] * b.m[1][j] +
                             a.m[i][2] * b.m[2][j] +
                             a.m[i][3] * b.m[3][j];
        }
    }

    return result;
}
