#pragma once
#include <list>
#include <SFML/Graphics.hpp>
#include <SFML/System.hpp>

namespace proto {

struct Cannonball {
	std::size_t id;
	sf::Sprite sprite;
	sf::Vector2f direction;
};

class CannonballSystem
	: public sf::Drawable {
	
	private:
		sf::Texture const & tex;
		std::size_t next_id;
		std::list<Cannonball> balls;
		
		void draw(sf::RenderTarget& target, sf::RenderStates states) const override;
		
	public:
		CannonballSystem(sf::Texture const & tex);
		
		std::size_t create(sf::Vector2f position, float angle);
		void destroy(std::size_t id);
		void update(sf::Time elapsed);
};

} // ::proto
