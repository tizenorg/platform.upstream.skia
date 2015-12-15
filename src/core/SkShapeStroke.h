/*
 * Copyright 2014 Samsung Electronics Inc.
 *
 * Use of this source code is governed by a BSD-style license that can be
 * found in the LICENSE file.
 */

#ifndef SkShapeStroke_DEFINED
#define SkShapeStroke_DEFINED

#include "SkPath.h"
#include "SkPoint.h"
#include "SkPaint.h"

/** Class SkShapeStroke
    SkShapeStroke is the utility class that constructs paths by stroking
    geometries (lines, rects, ovals, roundrects, paths). This is
    invoked when a geometry or text is drawn in a canvas with the
    kStroke_Mask bit set in the paint.
*/
class SkShapeStroke {
public:
    SkShapeStroke();
    SkShapeStroke(const SkPaint&);
    SkShapeStroke(const SkPaint&, SkScalar width);   // Width overrides paint.getStrokeWidth()

    SkPaint::Cap getCap() const { return (SkPaint::Cap)fCap; }
    SkPaint::Join getJoin() const { return (SkPaint::Join)fJoin; }
    void setCap(SkPaint::Cap);

    void setJoin(SkPaint::Join);

    void setMiterLimit(SkScalar);
    void setWidth(SkScalar);

    void strokePath(const SkPath& path, SkPath*, SkPath*, SkPath*) const;

    ////////////////////////////////////////////////////////////////

private:
    SkScalar    fWidth, fMiterLimit;
    uint8_t     fCap, fJoin;
    SkBool8     fDoFill;

    friend class SkPaint;
};

#endif
