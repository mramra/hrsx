
frappe.ui.form.on('Leave Application', {
	// refresh: function(frm) {

	// }
 to_date: function (frm) {
        frappe.call({
            method:"human_resource.human_resource.doctype.leave_application.leave_application.get_total_leave",
            args: {
                employee: frm.doc.employee,
                leave_type: frm.doc.leave_type,
                from_date: frm.doc.from_date,
                to_date: frm.doc.to_date
            },
            callback: (r) =>{
                //console.log(r.massage);
                frm.doc.leave_balance_before_application = r.massage;
            }

    })
    },


});