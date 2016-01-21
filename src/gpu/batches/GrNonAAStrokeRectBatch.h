/*
 * Copyright 2015 Google Inc.
 *
 * Use of this source code is governed by a BSD-style license that can be
 * found in the LICENSE file.
 */

#ifndef GrNonAAStrokeRectBatch_DEFINED
#define GrNonAAStrokeRectBatch_DEFINED

#include "GrColor.h"
#include "SkTypes.h"

class GrContext;
class GrDrawBatch;
struct SkRect;
class SkMatrix;

namespace GrNonAAStrokeRectBatch {

GrDrawBatch* Create(GrColor color,
                    const SkMatrix& viewMatrix,
                    const SkRect& rect,
                    SkScalar strokeWidth,
                    bool snapToPixelCenters,
                    GrContext *ctx,
                    bool isLine = false);

void Append(GrColor color,
            const SkMatrix& viewMatrix,
            const SkRect& rect,
            SkScalar strokeWidth,
            bool snapToPixelCenters);

};

#endif
