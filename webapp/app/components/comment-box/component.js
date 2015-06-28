import Ember from 'ember';

export default Ember.Component.extend({
    comment: null,

    canComment: function() {
        return Ember.$.trim(this.get('commentText')) !== '';
    }.property('commentText'),


    defineProperties: function() {
        Ember.defineProperty(this, 'commentText', Ember.computed.alias('comment.comment'));
        Ember.defineProperty(this, 'commentEdited', Ember.computed.alias('comment.edited'));
  }.on('init'),


    email: function() {
        if (this.get('commentEdited')) {
            return this.get('session.content.user_info.email');
        }
        return this.get('comment').get('user_email');
    }.property('commentEdited'),

    mine: function() {
        return this.get('comment.user_email') === this.get('session.content.user_info.email');
    }.property(),

    actions: {
        save: function() {
            this.sendAction('saveComment', this.get('comment'));
        }
    }
});