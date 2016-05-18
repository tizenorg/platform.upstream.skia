/*
    Copyright (c) 2013 250bpm s.r.o.  All rights reserved.

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"),
    to deal in the Software without restriction, including without limitation
    the rights to use, copy, modify, merge, publish, distribute, sublicense,
    and/or sell copies of the Software, and to permit persons to whom
    the Software is furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included
    in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
    THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
    IN THE SOFTWARE.
*/

#ifndef NN_FSM_INCLUDED
#define NN_FSM_INCLUDED

#include "../utils/queue.h"

/*  Base class for state machines. */

struct nn_ctx;
struct nn_fsm;
struct nn_worker;

struct nn_fsm_event {
    struct nn_fsm *fsm;
    int src;
    void *srcptr;
    int type;
    struct nn_queue_item item;
};

void nn_fsm_event_init (struct nn_fsm_event *self);
void nn_fsm_event_term (struct nn_fsm_event *self);
int nn_fsm_event_active (struct nn_fsm_event *self);
void nn_fsm_event_process (struct nn_fsm_event *self);

/*  Special source for actions. It's negative not to clash with user-defined
    sources. */
#define NN_FSM_ACTION -2

/*  Actions generated by fsm object. The values are negative not to clash
    with user-defined actions. */
#define NN_FSM_START -2
#define NN_FSM_STOP -3

/*  Virtual function to be implemented by the derived class to handle the
    incoming events. */
typedef void (*nn_fsm_fn) (struct nn_fsm *self, int src, int type,
    void *srcptr);

struct nn_fsm_owner {
    int src;
    struct nn_fsm *fsm;
};

struct nn_fsm {
    nn_fsm_fn fn;
    nn_fsm_fn shutdown_fn;
    int state;
    int src;
    void *srcptr;
    struct nn_fsm *owner;
    struct nn_ctx *ctx;
    struct nn_fsm_event stopped;
};

void nn_fsm_init_root (struct nn_fsm *self, nn_fsm_fn fn,
    nn_fsm_fn shutdown_fn, struct nn_ctx *ctx);
void nn_fsm_init (struct nn_fsm *self, nn_fsm_fn fn,
    nn_fsm_fn shutdown_fn,
    int src, void *srcptr, struct nn_fsm *owner);
void nn_fsm_term (struct nn_fsm *self);

int nn_fsm_isidle (struct nn_fsm *self);
void nn_fsm_start (struct nn_fsm *self);
void nn_fsm_stop (struct nn_fsm *self);
void nn_fsm_stopped (struct nn_fsm *self, int type);
void nn_fsm_stopped_noevent (struct nn_fsm *self);

/*  Replaces current owner of the fsm by the owner speicified by 'owner'
    parameter. The parameter will hold the old owner afrer the call. */
void nn_fsm_swap_owner (struct nn_fsm *self, struct nn_fsm_owner *owner);

struct nn_worker *nn_fsm_choose_worker (struct nn_fsm *self);

/*  Using this function state machine can trigger an action on itself. */
void nn_fsm_action (struct nn_fsm *self, int type);

/*  Send event from the state machine to its owner. */
void nn_fsm_raise (struct nn_fsm *self, struct nn_fsm_event *event, int type);


/*  Send event to the specified state machine. It's caller's responsibility
    to ensure that the destination state machine will still exist when the
    event is delivered.
    NOTE: This function is a hack to make inproc transport work in the most
    efficient manner. Do not use it outside of inproc transport! */
void nn_fsm_raiseto (struct nn_fsm *self, struct nn_fsm *dst,
    struct nn_fsm_event *event, int src, int type, void *srcptr);

/*  This function is very lowlevel action feeding
    Used in worker threads and timers, shouldn't be used by others
    use nn_fsm_action/nn_fsm_raise/nn_fsm_raiseto instread*/
void nn_fsm_feed (struct nn_fsm *self, int src, int type, void *srcptr);

#endif

