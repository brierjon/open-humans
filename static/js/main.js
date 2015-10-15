'use strict';

var $ = window.jQuery = require('jquery');

var Cookies = require('js-cookie');

require('bootstrap');
require('parsleyjs');
require('webshim');

// Specifically so IE will support the HTML5 form attribute on <input> elements
webshim.setOptions('basePath', '/static/vendor/shims/');
webshim.polyfill('forms');

function parsleyForm(element) {
  return $(element).parsley({
    successClass: 'has-success',
    errorClass: 'has-error',
    trigger: 'change keyup focusout',
    classHandler: function (field) {
      if (field.$element.attr('type') === 'radio') {
        return $('input[type=radio][name=' + field.$element.attr('name') + ']')
          .parents('.radio');
      }

      return field.$element.parents('.form-group');
    },
    errorsContainer: function (field) {
      var $field = field.$element;

      if (field.$element.attr('type') === 'radio') {
        $field = $('input[type=radio][name=' + field.$element.attr('name') +
          ']:last').parent().parent();

        return $('<span></span>').insertAfter($field);
      }

      if (field.$element.parent('.input-group')) {
        $field = field.$element.parent('.input-group');
      }

      return $('<span></span>').insertAfter($field);
    },
    errorsWrapper: '<span class="help-block"></span>',
    errorTemplate: '<div></div>'
  });
}

function csrfSafeMethod(method) {
  // These HTTP methods do not require CSRF protection
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

var csrfToken = Cookies.get('csrftoken');

$.ajaxSetup({
  beforeSend: function (xhr, settings) {
    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
      xhr.setRequestHeader('X-CSRFToken', csrfToken);
    }
  }
});

function showModal(modalId) {
  return function (e) {
    // Allow for middle-clicking, control-clicking, and command-clicking
    if (e.isDefaultPrevented() || e.metaKey || e.ctrlKey) {
      return;
    }

    e.preventDefault();

    $(modalId).modal({remote: false});
  };
}

$(function () {
  parsleyForm('form');

  $('.logout-link').click(function (e) {
    e.preventDefault();

    $.post($(this).attr('href'), function () {
      location.reload();
    });
  });

  // Add these modals with JavaScript rather than data- attributes to prevent
  // AJAX loading of modal content by Bootstrap.
  $('.login-link').click(showModal('#login-modal'));
  $('.signup-link').click(showModal('#signup-modal'));
});
