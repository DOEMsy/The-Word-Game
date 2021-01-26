//
// Created by DOEMsy on 2021/1/5.
//

#include "ExternalLibrary.h"

vector<string> ExternalLibrary::SPLIT(const string &s, char c) {
    vector<string> res;
    string tmp;
    for (auto &it:s) {
        if (it == c) {
            if (!tmp.empty()) {
                res.push_back(tmp);
                tmp = "";
            }
        } else {
            tmp += it;
        }
    }

    return res;
}

int ExternalLibrary::INT(const string &s) {
    int res = 0;
    for (auto &it : s) {
        if ('0' <= it && it <= '9') {
            res *= 10;
            res += it - '0';
        }
    }
    return res;
}

vector<int> ExternalLibrary::INT(const vector<string>& vs) {
    vector<int> res;
    for (auto &s:vs)
        res.push_back(INT(s));
    return res;
}

template<class T>
vector<T> ExternalLibrary::SUBVEC(const vector<T> &v, int begin, int len) {
    int sz = v.size();
    if(begin>=v.size()) return vector<T>();
    auto bg = v.begin() + begin;
    auto ed = v.begin() + begin;
    if(len==-1 || begin+len > sz){
        ed = v.end();
    }
    return vector<T>(bg,ed);
}

template<typename Type, typename... Types>
int ExternalLibrary::log(const Type &arg, const Types &... args) {
    std::cout << arg << " ";
    log(args...);
    return 1;
}

template<typename Type, typename... Types>
int ExternalLibrary::LOG(const Type &arg, const Types &... args) {
    log(args...);
    std::cout<<endl;
    return 1;
}


