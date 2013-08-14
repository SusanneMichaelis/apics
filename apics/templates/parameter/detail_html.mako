<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "parameters" %>
<%block name="title">${ctx.id} ${ctx.__unicode__()}</%block>

<ul class="nav nav-pills pull-right">
    <li><a href="#map-container">Map</a></li>
    <li><a href="#list-container">List</a></li>
</ul>

<h2>${title()}</h2>

<div class="row-fluid">
    % if ctx.description:
    <div class="span8">
        <h3>Description</h3>
        ${h.text2html(ctx.markup_description or ctx.description, mode='p', sep='\n')}
    </div>
    % endif
    <div class="span4">
        % if ctx.authors:
        <%util:well title="Author">
            <span>${ctx.format_authors()}</span>
            ${h.button('cite', id="cite-button", onclick=h.JSModal.show(ctx.name, request.resource_url(ctx, ext='md.html')))}
        </%util:well>
        % endif
        <%util:well title="Values">
            ${u.value_table(ctx, request)}
        </%util:well>
    </div>
</div>

${request.map.render()}

<div id="list-container">
    <% dt = request.registry.getUtility(h.interfaces.IDataTable, 'values'); dt = dt(request, h.models.Value, parameter=ctx) %>
    ${dt.render()}
</div>
