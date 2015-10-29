#pragma once
#include <SFML/Graphics.hpp>
#include <SFML/System.hpp>

namespace proto {

class Ship
	: public sf::Drawable {
	private:
		sf::Vector2f position, rotation;
		float angle, delta;
		bool moving;
		sf::Sprite sprite;
		
		void draw(sf::RenderTarget& target, sf::RenderStates states) const override;
		
	public:
		Ship(sf::Vector2f position, sf::Texture const & tex);
		
		sf::Vector2f getPosition() const;
		
		void rotate(float delta);
		void move();
		void stop();
		void update(sf::Time elapsed);
};

} // ::proto
