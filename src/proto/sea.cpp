#include <proto/sea.hpp>

namespace proto {

Sea::Sea(sf::Texture const & tex)
	: sf::Drawable{}
	, tiles{sf::Quads}
	, tex{tex} {
	auto tilesize = sf::Vector2f{tex.getSize()};
	for (auto y = 0u; y < 10u; ++y) {
		for (auto x = 0u; x < 10u; ++x) {
			tiles.append({{x * tilesize.x, y * tilesize.y}, {0.f, 0.f}});
			tiles.append({{(x+1) * tilesize.x, y * tilesize.y}, {tilesize.x, 0.f}});
			tiles.append({{(x+1) * tilesize.x, (y+1) * tilesize.y}, tilesize});
			tiles.append({{x * tilesize.x, (y+1) * tilesize.y}, {0.f, tilesize.y}});
		}
	}
}

void Sea::draw(sf::RenderTarget& target, sf::RenderStates states) const {
	states.texture = &tex;
	target.draw(tiles, states);
}

} // ::proto
