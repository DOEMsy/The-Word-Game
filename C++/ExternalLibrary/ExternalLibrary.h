//
// Created by DOEMsy on 2021/1/5.
//

#ifndef THE_WORD_GAME_EXTERNALLIBRARY_H
#define THE_WORD_GAME_EXTERNALLIBRARY_H

#include "bits/stdc++.h"

using namespace std;

class ExternalLibrary {
private:
    template<typename Type, typename... Types>
    static int log(const Type& arg, const Types&... args);
public:
    static vector<string> SPLIT(const string &, char c = ' ');

    static int INT(const string &);

    static vector<int> INT(const vector<string>&);

    template<class T>
    static vector<T> SUBVEC(const vector<T> &v, int begin, int len = -1);

    template<typename Type, typename... Types>
    static int LOG(const Type& arg, const Types&... args);

};


#endif //THE_WORD_GAME_EXTERNALLIBRARY_H
