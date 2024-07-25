/* vector_utils.hpp - Vector Utility Function Templates */
#ifndef VECTOR_UTILS_HPP
#define VECTOR_UTILS_HPP

#include <vector>

#include <cmath>
#include <algorithm>

#include <stdexcept>

#include <ostream>
#include <sstream>
#include <iomanip>

/* Vector Slicing*/
template <typename T>
std::vector<T> slice(std::vector<T> const& v, int i, int j) {
    std::vector<T> vec(v.begin() + i, v.begin() + j + 1);
    return vec;
}

/* Vector Operations*/
template <typename T>
std::vector<T> operator +(std::vector<T> const& v1, std::vector<T> const& v2) {
    // Element wise subtraction of the second argument from the first
    if (v1.size() != v1.size()) {
        throw std::invalid_argument("Vectors must be of the same size");
    }

    std::vector<T> v(v1.size(), 0);
    for (int i=0; i < (int)(v1.size()); i++) {
        v[i] = v1[i] + v2[i];
    }

    return v;
}

template <typename T>
std::vector<T> operator -(std::vector<T> const& v1, std::vector<T> const& v2) {
    // Element wise subtraction of the second argument from the first
    if (v1.size() != v1.size()) {
        throw std::invalid_argument("Vectors must be of the same size");
    }

    std::vector<T> v(v1.size(), 0);
    for (int i=0; i < (int)(v1.size()); i++) {
        v[i] = v1[i] - v2[i];
    }

    return v;
}

/* Vector p-Norms */
template <typename T>
T norm(std::vector<T> const& v, double p=2) {
    // Compute the p-norm of a vector
    if (p < 1) {
        throw std::invalid_argument("p should be from [1,inf)");
    }

    T val = 0;
    for(const T& ele : v) {
            val += std::pow(std::abs(ele), p);
    }
        
    return std::pow(val, 1/p);
}

template <typename T>
T norm(std::vector<T> const& v, std::string p) {
    // Compute the p-norm of a vector
    if (p.compare("inf") != 0) {
        throw std::invalid_argument("std::string p must be inf");
    }

    return std::abs(*max_element(v.begin(), v.end(), 
        [](const double& a, const double& b){
            return abs(a) < abs(b);
    }));
}

/* Vector Generators */
template <typename T>
std::vector<T> linspace(T a, T b, size_t N) {
    T h = (b-a) / static_cast<T>(N-1);
    std::vector<T> vec(N,0);
    
    auto it = vec.begin();
    T vi = a;
    for (; it != vec.end(); ++it, vi+=h) {
        *it = vi;
    }
    return vec;
}

/* Vector Reporting */
template <typename T>
std::ostream& operator <<(std::ostream& os, std::vector<T> const& v) {
    auto w = os.width();
    auto p = os.precision();

    std::stringstream ss;
    ss << std::fixed << std::setprecision(p) << std::setfill(' ');

    ss << std::setw(0) << "[";
    for (const T& ele : v) {
        ss << " " << std::setw(w) << ele;
    }
    ss << " ]";

    os << std::setw(0) << ss.rdbuf() << std::setw(w);
    return os;
}

#endif