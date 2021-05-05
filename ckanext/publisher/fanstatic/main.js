"use strict";

/*
 *
 * This JavaScript module adds ajax support for the publish and unpublish button on the read_base_snippet.html file
 * When the user clicks the button the data will be sent to this file and proccessed.
 * on the HTML element to show the popover.
 *
 * id - the id of the dataset
 * is_private - the visibilty of the dataset, either true or false
 *
 */

ckan.module('publisher_main', function ($) {
    return {
        initialize: function () {

            // proxyAll() ensures that whenever an _on*() function from this
            // JavaScript module is called, the `this` variable in the function will
            // be this JavaScript module object.
            //
            // You probably want to call proxyAll() like this in the initialize()
            // function of most modules.
            //
            // This is a shortcut function provided by CKAN, it wraps jQuery's
            // proxy() function: http://api.jquery.com/jQuery.proxy/
            $.proxyAll(this, /_on/);


            // Add an event handler to the button, when the user clicks the button
            // our _onClick() function will be called.
            this.el.on('click', this._onClick);
        },


        _onClick: function (event) {

            // Send an ajax request to CKAN to render the popover.html snippet.
            // We wrap this in an if statement because we only want to request
            // the snippet from CKAN once, not every time the button is clicked.
            if (!this._snippetReceived) {
                var isprivate = this.options.isprivate;
                var id = this.options.id;
                var root_path = this.options.url;
                var data = {
                    "private": isprivate,
                    "id": id
                };

                updateMetaData(isprivate, data,root_path);
            }
        },


    };
});


function updateMetaData(isprivate, data,root_path) {
    //TODO check pop consitency in the application and apply ajax call to the publish or unpublish button
    $.ajax({
        url: root_path,
        data: JSON.stringify(data),
        dataType: "json",
        type: 'POST',
        contentType: 'application/json',
        success: function (response) {
            //TODO GO TO {hostname}/dataset/{dataset-id or name}
            location.reload();
        }
        ,
        error: function (e) {
            console.log(e);
            //TODO enable the button



        }
    });
    //TODO status of the button disabled
}
