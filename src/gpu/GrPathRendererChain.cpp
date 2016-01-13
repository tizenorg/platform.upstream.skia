
/*
 * Copyright 2011 Google Inc.
 *
 * Use of this source code is governed by a BSD-style license that can be
 * found in the LICENSE file.
 */


#include "GrPathRendererChain.h"

#include "GrCaps.h"
#include "GrContext.h"
#include "GrHairLinePathRenderer.h"
#include "GrShapePathRenderer.h"
#include "GrGpu.h"
#include "GrHairLinePathRenderer.h"

#include "batches/GrAAConvexPathRenderer.h"
#include "batches/GrAADistanceFieldPathRenderer.h"
#include "batches/GrAAHairLinePathRenderer.h"
#include "batches/GrAALinearizingConvexPathRenderer.h"
#include "batches/GrDashLinePathRenderer.h"
#include "batches/GrDefaultPathRenderer.h"
#include "batches/GrStencilAndCoverPathRenderer.h"
#include "batches/GrTessellatingPathRenderer.h"

GrPathRendererChain::GrPathRendererChain(GrContext* context)
    : fInit(false)
    , fOwner(context) {
}

GrPathRendererChain::~GrPathRendererChain() {
    for (int i = 0; i < fChain.count(); ++i) {
        fChain[i]->unref();
    }
}

GrPathRenderer* GrPathRendererChain::addPathRenderer(GrPathRenderer* pr) {
    fChain.push_back() = pr;
    pr->ref();
    return pr;
}

GrPathRenderer* GrPathRendererChain::getPathRenderer(const GrDrawTarget* target,
                                                     const GrPipelineBuilder* pipelineBuilder,
                                                     const SkMatrix& viewMatrix,
                                                     const SkPath& path,
                                                     const GrStrokeInfo& stroke,
                                                     DrawType drawType,
                                                     StencilSupport* stencilSupport) {
    if (!fInit) {
        this->init();
    }
    bool antiAlias = (kColorAntiAlias_DrawType == drawType ||
                      kStencilAndColorAntiAlias_DrawType == drawType);

    GR_STATIC_ASSERT(GrPathRenderer::kNoSupport_StencilSupport <
                     GrPathRenderer::kStencilOnly_StencilSupport);
    GR_STATIC_ASSERT(GrPathRenderer::kStencilOnly_StencilSupport <
                     GrPathRenderer::kNoRestriction_StencilSupport);
    GrPathRenderer::StencilSupport minStencilSupport;
    if (kStencilOnly_DrawType == drawType) {
        minStencilSupport = GrPathRenderer::kStencilOnly_StencilSupport;
    } else if (kStencilAndColor_DrawType == drawType ||
               kStencilAndColorAntiAlias_DrawType == drawType) {
        minStencilSupport = GrPathRenderer::kNoRestriction_StencilSupport;
    } else {
        minStencilSupport = GrPathRenderer::kNoSupport_StencilSupport;
    }


    for (int i = 0; i < fChain.count(); ++i) {
        GrPathRenderer::CanDrawPathArgs args;
        args.fShaderCaps = target->caps()->shaderCaps();
        args.fPipelineBuilder = pipelineBuilder;
        args.fViewMatrix = &viewMatrix;
        args.fPath = &path;
        args.fStroke = &stroke;
        args.fAntiAlias = antiAlias;
        if (fChain[i]->canDrawPath(args)) {
            if (GrPathRenderer::kNoSupport_StencilSupport != minStencilSupport) {
                GrPathRenderer::StencilSupport support =
                                                       fChain[i]->getStencilSupport(path, stroke);
                if (support < minStencilSupport) {
                    continue;
                } else if (stencilSupport) {
                    *stencilSupport = support;
                }
            }
            return fChain[i];
        }
    }
    return nullptr;
}

GrPathRenderer* GrPathRendererChain::getPathRenderer(const SkPath& pathA,
                                                     const SkPath& pathB,
                                                     const SkPath& pathC,
                                                     const GrStrokeInfo& stroke,
                                                     const GrDrawTarget* target,
                                                     GrPipelineBuilder* pipelineBuilder,
                                                     const SkMatrix& viewMatrix,
                                                     DrawType drawType,
                                                     StencilSupport* stencilSupport) {
    if (!fInit) {
        this->init();
    }
    bool antiAlias = (kColorAntiAlias_DrawType == drawType ||
                      kStencilAndColorAntiAlias_DrawType == drawType);

    GR_STATIC_ASSERT(GrPathRenderer::kNoSupport_StencilSupport <
                     GrPathRenderer::kStencilOnly_StencilSupport);
    GR_STATIC_ASSERT(GrPathRenderer::kStencilOnly_StencilSupport <
                     GrPathRenderer::kNoRestriction_StencilSupport);
    GrPathRenderer::StencilSupport minStencilSupport;
    if (kStencilOnly_DrawType == drawType) {
        minStencilSupport = GrPathRenderer::kStencilOnly_StencilSupport;
    } else if (kStencilAndColor_DrawType == drawType ||
               kStencilAndColorAntiAlias_DrawType == drawType) {
        minStencilSupport = GrPathRenderer::kNoRestriction_StencilSupport;
    } else {
        minStencilSupport = GrPathRenderer::kNoSupport_StencilSupport;
    }


    for (int i = 0; i < fChain.count(); ++i) {
        GrColor color = GrColor_ILLEGAL;
        if (fChain[i]->canDrawPath(pathA, pathB, pathC, stroke, target,
                                   pipelineBuilder, color, viewMatrix, antiAlias)) {
            if (GrPathRenderer::kNoSupport_StencilSupport != minStencilSupport) {
                GrPathRenderer::StencilSupport support = fChain[i]->getStencilSupport(pathA, stroke);
                if (support < minStencilSupport) {
                    continue;
                } else if (NULL != stencilSupport) {
                    *stencilSupport = support;
                }
            }
            return fChain[i];
        }
    }
    return NULL;
}

void GrPathRendererChain::init() {
    SkASSERT(!fInit);
    const GrCaps& caps = *fOwner->caps();
    this->addPathRenderer(new GrHairLinePathRenderer)->unref();
    this->addPathRenderer(new GrDashLinePathRenderer)->unref();

    if (GrPathRenderer* pr = GrStencilAndCoverPathRenderer::Create(fOwner->resourceProvider(),
                                                                   caps)) {
        this->addPathRenderer(pr)->unref();
    }
    this->addPathRenderer(new GrAAHairLinePathRenderer)->unref();
    this->addPathRenderer(new GrAAConvexPathRenderer)->unref();
    this->addPathRenderer(new GrAALinearizingConvexPathRenderer)->unref();
    this->addPathRenderer(new GrAADistanceFieldPathRenderer)->unref();
    this->addPathRenderer(new GrShapePathRenderer)->unref();
    this->addPathRenderer(new GrDefaultPathRenderer(caps.twoSidedStencilSupport(),
                                                    caps.stencilWrapOpsSupport()))->unref();
    this->addPathRenderer(new GrTessellatingPathRenderer)->unref();
    fInit = true;
}
