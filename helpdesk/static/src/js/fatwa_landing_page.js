// odoo.define('landing.page', function (require) {
//     "use strict";
    
//     /**
//      * This file defines the Helpdesk Dashboard view (alongside its renderer, model
//      * and controller), extending the Kanban view.
//      * The Helpdesk Dashboard view is registered to the view registry.
//      * A large part of this code should be extracted in an AbstractDashboard
//      * widget in web, to avoid code duplication (see SalesTeamDashboard).
//      */
    
//     var core = require('web.core');
//     var rpc = require('web.rpc');
//     var KanbanController = require('web.KanbanController');
//     var session = require('web.session');
    
//     var _t = core._t;
    
//     var FatwaLandingPageController = KanbanController.extend({
//         custom_events: _.extend({}, KanbanController.prototype.custom_events, {
//             dashboard_open_action: '_onDashboardOpenAction',
//             dashboard_edit_target: '_onDashboardEditTarget',
//         }),
    
//         //--------------------------------------------------------------------------
//         // Handlers
//         //--------------------------------------------------------------------------
//         /**
//          * @private
//          * @param {OdooEvent} e
//          */
//         _onSearchAction: function (e) {
//             var external_id = 'model.action_id';
//             var model = 'ir.actions.act_window'; //helpdesk.ticket
//             this._rpc({
//                     model: model,
//                     method: 'search',
//                     args: [['xml_id', '=', helpdesk.helpdesk_ticket_action_main]],
//                     context: session.user_context,
//                 }).then(function(ids) {
//                             if (ids.length > 0) {
//                             var action_id = ids[0];
//                             console.log('Action ID: ' + action_id);
//                             return action_id;
//                         }
//             })
//             .then(this.reload.bind(this));
//         },
//     });
    
//     return {
//         Controller: FatwaLandingPageController
//     };
    
//     });
    