#pragma once
#include <SFML/Graphics.hpp>
#include <SFML/System.hpp>

namespace proto {

class Sea
	: public sf::Drawable {
	private:
		sf::VertexArray tiles;
		sf::Texture const & tex;
		
		void draw(sf::RenderTarget& target, sf::RenderStates states) const override;
		
	public:
		Sea(sf::Texture const & tex);
};

} // ::proto
