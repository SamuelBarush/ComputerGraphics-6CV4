#include "vector.h"
#include <math.h>

//Vector 2D funtions
float vec2_length (vec2_t v){
    return sqrt(v.x * v.x + v.y * v.y);
}

vec2_t vec2_add (vec2_t a, vec2_t b){
    vec2_t result =  {a.x + b.x, a.y + b.y};
    return result;
}

vec2_t vec2_sub (vec2_t a, vec2_t b){
    vec2_t result =  {a.x - b.x, a.y - b.y};
    return result;
}

vec2_t vec2_mul (vec2_t a, float factor){
    vec2_t result =  {a.x * factor, a.y * factor};
    return result;
}

vec2_t vec2_div (vec2_t a, float factor){
    vec2_t result =  {a.x / factor, a.y / factor};
    return result;
}

void vec2_normilize (vec2_t* v){
    float length = vec2_length(*v);
    if  (length != 0){
        v->x /= length;
        v->y /= length;
    }
}

//Vector 3D funtions
float vec3_length (vec3_t v){
    return sqrt(v.x * v.x + v.y * v.y + v.z * v.z);
}

vec3_t vec3_add (vec3_t a, vec3_t b){
    vec3_t result = {a.x + b.x, a.y + b.y, a.z + b.z};
    return result;
}

vec3_t vec3_sub (vec3_t a, vec3_t b){
    vec3_t result = {a.x - b.x, a.y - b.y, a.z - b.z};
    return result;
}

vec3_t vec3_mul (vec3_t a, float factor){
    vec3_t result = {a.x * factor, a.y * factor, a.z * factor};
    return result;
}

vec3_t vec3_div (vec3_t a, float factor){
    vec3_t result = {a.x / factor, a.y / factor, a.z / factor};
    return result;
}

vec3_t vec3_cross (vec3_t a, vec3_t b){
    vec3_t result = {
        a.y * b.z - a.z * b.y,
        a.z * b.x - a.x * b.z,
        a.x * b.y - a.y * b.x
    };
    return result;
}

float vec3_dot(vec3_t a, vec3_t b) {
    return a.x * b.x + a.y * b.y + a.z * b.z;
}

void vec3_normalize(vec3_t* v) {
    float length = vec3_length(*v);
    if (length != 0) {
        v->x /= length;
        v->y /= length;
        v->z /= length;
    }
}

vec3_t vec3_rotate_x(vec3_t v, float angle) {
    float cos_theta = cosf(angle);
    float sin_theta = sinf(angle);
    vec3_t result = {
        v.x,
        v.y * cos_theta - v.z * sin_theta,
        v.y * sin_theta + v.z * cos_theta
    };
    return result;
}

vec3_t vec3_rotate_y(vec3_t v, float angle) {
    float cos_theta = cosf(angle);
    float sin_theta = sinf(angle);
    vec3_t result = {
        v.x * cos_theta + v.z * sin_theta,
        v.y,
        -v.x * sin_theta + v.z * cos_theta
    };
    return result;
}

vec3_t vec3_rotate_z(vec3_t v, float angle) {
    float cos_theta = cosf(angle);
    float sin_theta = sinf(angle);
    vec3_t result = {
        v.x * cos_theta - v.y * sin_theta,
        v.x * sin_theta + v.y * cos_theta,
        v.z
    };
    return result;
}

// Vector conversion functions
vec4_t vec4_from_vec3(vec3_t v) {
    vec4_t result = {v.x, v.y, v.z, 1.0f};
    return result;
}

vec3_t vec3_from_vec4(vec4_t v) {
    vec3_t result = {v.x, v.y, v.z};
    return result;
}

