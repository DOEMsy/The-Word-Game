//
// Created by DOEMsy on 2021/1/2.
//

#include "Labels.h"

bool Is(label lab, const UnitCard& ut) {
    if (lab % 10 == 0) {
        for (int i = 1; i < 10; i++) {
            if (ut.Label.count(++lab)) {
                return true;
            }
        }
        return false;
    } else {
        return ut.Label.count(lab);
    }
}

bool Is(label lab, const StatusEffect& se) {
    if (lab % 10 == 0) {
        for (int i = 1; i < 10; i++) {
            if (se.Attrs.count(++lab)) {
                return true;
            }
        }
        return false;
    } else {
        return se.Attrs.count(lab);
    }
}
