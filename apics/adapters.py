from clld import interfaces
from clld.web.adapters import GeoJsonParameter
from clld.web.adapters.md import BibTex, TxtCitation
from clld.web.adapters.base import Representation
from clld.lib import bibtex


class GeoJsonFeature(GeoJsonParameter):
    def feature_iterator(self, ctx, req):
        for vs in super(GeoJsonFeature, self).feature_iterator(ctx, req):
            if not vs.language.language_pk:
                yield vs


class GeoJsonApicsWals(GeoJsonParameter):
    def featurecollection_properties(self, ctx, req):
        return self.obj

    def feature_properties(self, ctx, req, vs):
        return {'icon': self.obj['icon']}

    def feature_iterator(self, ctx, req):
        return [vs for vs in ctx.valuesets
                if vs.jsondata.get('wals_value_number') == self.obj['number']
                and not vs.language.language_pk]


class FeatureMetadata(Representation):
    template = 'md_html.mako'
    mimetype = 'application/vnd.clld.md+xml'
    extension = 'md.html'


class FeatureBibTex(BibTex):
    def rec(self, ctx, req):
        return bibtex.Record(
            'incollection',
            ctx.id,
            title=getattr(ctx, 'citation_name', ctx.__unicode__()),
            url=req.resource_url(ctx),
            address=req.dataset.publisher_place,
            publisher=req.dataset.publisher_name,
            year=str(req.dataset.published.year),
            author=ctx.format_authors(),
            booktitle=req.dataset.description,
            editor=' and '.join(c.contributor.name for c in list(req.dataset.editors)))


class FeatureReferenceManager(FeatureBibTex):
    """Resource metadata in RIS format.
    """
    name = 'RIS'
    __label__ = 'RIS'
    unapi = 'ris'
    extension = 'md.ris'
    mimetype = "application/x-research-info-systems"

    def render(self, ctx, req):
        return self.rec(ctx, req).format('ris')


class FeatureTxtCitation(TxtCitation):
    def render(self, ctx, req):
        self.template = 'parameter/md_txt.mako'
        return Representation.render(self, ctx, req)


def includeme(config):
    config.register_adapter(GeoJsonFeature, interfaces.IParameter)
    config.register_adapter(FeatureMetadata, interfaces.IParameter)
    for cls in [FeatureBibTex, FeatureTxtCitation, FeatureReferenceManager]:
        for if_ in [interfaces.IRepresentation, interfaces.IMetadata]:
            config.register_adapter(cls, interfaces.IParameter, if_)
