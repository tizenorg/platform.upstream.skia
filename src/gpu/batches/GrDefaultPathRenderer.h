/*
 * Copyright 2011 Google Inc.
 *
 * Use of this source code is governed by a BSD-style license that can be
 * found in the LICENSE file.
 */

#ifndef GrDefaultPathRenderer_DEFINED
#define GrDefaultPathRenderer_DEFINED

#include "GrPathRenderer.h"
#include "SkTypes.h"

/**
 *  Subclass that renders the path using the stencil buffer to resolve fill rules
 * (e.g. winding, even-odd)
 */
class SK_API GrDefaultPathRenderer : public GrPathRenderer {
public:
    GrDefaultPathRenderer(bool separateStencilSupport, bool stencilWrapOpsSupport);

private:

    StencilSupport onGetStencilSupport(const SkPath&, const GrStrokeInfo&) const override;

    bool onCanDrawPath(const CanDrawPathArgs&) const override;

    bool onDrawPath(const DrawPathArgs&) override;

    void onStencilPath(const StencilPathArgs&) override;

    bool internalDrawPath(GrDrawTarget*,
                          GrPipelineBuilder*,
                          GrColor,
                          const SkMatrix& viewMatrix,
                          const SkPath&,
                          const GrStrokeInfo&,
                          bool stencilOnly);

    bool canDrawPath(const SkPath&,
                     const SkPath&,
                     const SkPath&,
                     const GrStrokeInfo&,
                     const GrDrawTarget*,
                     GrPipelineBuilder* pipelineBuilder,
                     GrColor color,
                     const SkMatrix& viewMatrix,
                     bool antiAlias) const override {
        return false;
    }

    bool onDrawPath(const SkPath&,
                    const SkPath&,
                    const SkPath&,
                    const GrStrokeInfo&,
                    GrDrawTarget*,
                    GrPipelineBuilder*,
                    GrColor color,
                    const SkMatrix& viewMatrix,
                    bool antiAlias) override {
        return false;
    }

    void onStencilPath(const SkPath&,
                       const SkPath&,
                       const SkPath&,
                       const GrStrokeInfo&,
                       GrDrawTarget*,
                       GrPipelineBuilder* pipelineBuilder,
                       GrColor color,
                       const SkMatrix& viewMatrix) {
        return;
    }

    bool    fSeparateStencil;
    bool    fStencilWrapOps;

    typedef GrPathRenderer INHERITED;
};

#endif
