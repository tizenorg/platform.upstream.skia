/*
 * Copyright 2014 Google Inc.
 *
 * Use of this source code is governed by a BSD-style license that can be
 * found in the LICENSE file.
 */

#include "GrCoordTransform.h"
#include "GrCaps.h"
#include "GrContext.h"
#include "GrGpu.h"

void GrCoordTransform::reset(GrCoordSet sourceCoords, const SkMatrix& m, const GrTexture* texture,
                             GrTextureParams::FilterMode filter) {
    SkASSERT(texture);
    SkASSERT(!fInProcessor);

    fSourceCoords = sourceCoords;
    fMatrix = m;
    fReverseY = kBottomLeft_GrSurfaceOrigin == texture->origin();

    // take highest supported precision possible to avoid generating different
    // version of shader code which triggers extra compilation/linking.
    fPrecision = kDefault_GrSLPrecision;
    if (texture->getContext()) {
        const GrShaderCaps* caps = texture->getContext()->caps()->shaderCaps();
        if (caps->floatPrecisionVaries()) {
            const GrShaderCaps::PrecisionInfo* info;
            GrSLPrecision nextP = kHigh_GrSLPrecision;
            do {
                info = &caps->getFloatShaderPrecisionInfo(kFragment_GrShaderType, nextP);
                if (info->supported()) {
                    fPrecision = nextP;
                    break;
                }
                SkASSERT(nextP > kLow_GrSLPrecision);
                nextP = static_cast<GrSLPrecision>(nextP - 1);
            } while (true);
        }
    }
}

void GrCoordTransform::reset(GrCoordSet sourceCoords,
                             const SkMatrix& m,
                             GrSLPrecision precision) {
    SkASSERT(!fInProcessor);
    fSourceCoords = sourceCoords;
    fMatrix = m;
    fReverseY = false;
    fPrecision = precision;
}
