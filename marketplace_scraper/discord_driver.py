import requests
import datetime
from typing import List, Dict, Any
from marketplace_scraper.matched_listings import MatchedListings


class DiscordClient:
    """
    A class for sending messages to Discord via webhooks.
    
    This class provides methods for sending various types of messages to Discord,
    including simple text messages, rich embeds, and customized notifications.
    """
    
    def __init__(
        self,
        webhook_url: str,
        username: str = None,
        avatar_url: str = None
    ):
        """
        Initialize the Discord webhook.
        
        Args:
            webhook_url (str): The Discord webhook URL
            username (str, optional): Custom username to display
            avatar_url (str, optional): URL to avatar image
        """
        self.webhook_url = webhook_url
        self.username = username
        self.avatar_url = avatar_url
    
    def send_message(
        self,
        content: str = None,
        embeds: List[Dict[str, Any]] = None,
        tts: bool = False,
        username: str = None,
        avatar_url: str = None
    ) -> requests.Response:
        """
        Send a message to Discord.
        
        Args:
            content (str, optional): Simple message content
            embeds (List[Dict], optional): List of rich embed objects
            tts (bool, optional): Text-to-speech flag
            username (str, optional): Override the default username
            avatar_url (str, optional): Override the default avatar URL
            
        Returns:
            requests.Response: The HTTP response from Discord
        """
        if not content and not embeds:
            raise ValueError("Either content or embeds must be provided")
        
        # Prepare payload
        payload = {}
        
        if content:
            payload["content"] = content
        
        if embeds:
            payload["embeds"] = embeds
        
        if tts:
            payload["tts"] = True
        
        # Set username and avatar_url if provided, otherwise use instance defaults
        if username or self.username:
            payload["username"] = username or self.username
        
        if avatar_url or self.avatar_url:
            payload["avatar_url"] = avatar_url or self.avatar_url
        
        # Send the request
        response = requests.post(self.webhook_url, json=payload)
        
        # Check for errors
        if response.status_code not in [200, 204]:
            print(f"Error sending message: {response.status_code} - {response.text}")
        
        return response
    
    def create_embed(
        self,
        title: str = None,
        description: str = None,
        url: str = None,
        timestamp: bool = True,
        color: int = None,
        footer: Dict[str, str] = None,
        image: Dict[str, str] = None,
        thumbnail: Dict[str, str] = None,
        author: Dict[str, str] = None,
        fields: List[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create a rich embed object.
        
        Args:
            title (str, optional): Embed title
            description (str, optional): Embed description
            url (str, optional): URL for the title to link to
            timestamp (bool, optional): Whether to include current timestamp
            color (int, optional): Color code in decimal (not hex)
            footer (Dict, optional): Footer with text and icon_url keys
            image (Dict, optional): Image with url key
            thumbnail (Dict, optional): Thumbnail with url key
            author (Dict, optional): Author with name, url, and icon_url keys
            fields (List[Dict], optional): List of field dicts with name, value, inline keys
            
        Returns:
            Dict: The formatted embed object
        """
        embed = {}
        
        if title:
            embed["title"] = title
        
        if description:
            embed["description"] = description
        
        if url:
            embed["url"] = url
        
        if timestamp:
            embed["timestamp"] = datetime.datetime.utcnow().isoformat()
        
        if color:
            embed["color"] = color
        
        if footer:
            embed["footer"] = footer
        
        if image:
            embed["image"] = image
        
        if thumbnail:
            embed["thumbnail"] = thumbnail
        
        if author:
            embed["author"] = author
        
        if fields:
            embed["fields"] = fields
        
        return embed
    
    def send_embed(
        self,
        title: str = None,
        description: str = None,
        color: int = None,
        fields: List[Dict[str, Any]] = None,
        **kwargs
    ) -> requests.Response:
        """
        Create and send an embed message.
        
        Args:
            title (str, optional): Embed title
            description (str, optional): Embed description
            color (int, optional): Color code in decimal
            fields (List[Dict], optional): List of field dicts
            **kwargs: Additional arguments for create_embed method
            
        Returns:
            requests.Response: The HTTP response from Discord
        """
        embed = self.create_embed(
            title=title,
            description=description,
            color=color,
            fields=fields,
            **kwargs
        )
        
        return self.send_message(embeds=[embed])
    
    # Convenience methods for different notification types
    
    def send_info(
        self,
        title: str,
        description: str = None,
        **kwargs
    ) -> requests.Response:
        """Send an information message (blue)"""
        return self.send_embed(
            title=title,
            description=description,
            color=3447003,  # Blue
            **kwargs
        )
    
    def send_success(
        self,
        title: str,
        description: str = None,
        **kwargs
    ) -> requests.Response:
        """Send a success message (green)"""
        return self.send_embed(
            title=title,
            description=description,
            color=5763719,  # Green
            **kwargs
        )
    
    def send_warning(
        self,
        title: str,
        description: str = None,
        **kwargs
    ) -> requests.Response:
        """Send a warning message (yellow)"""
        return self.send_embed(
            title=title,
            description=description,
            color=16776960,  # Yellow
            **kwargs
        )
    
    def send_error(
        self,
        title: str,
        description: str = None,
        **kwargs
    ) -> requests.Response:
        """Send an error message (red)"""
        return self.send_embed(
            title=title,
            description=description,
            color=15158332,  # Red
            **kwargs
        )


class Discord:
    """
    A driver class for sending marketplace listings to Discord.
    Similar to the Email class but for Discord notifications.
    """
    
    def __init__(self, webhook_url: str):
        """
        Initialize the Discord driver with a webhook URL.
        
        Args:
            webhook_url (str): The Discord webhook URL
        """
        self.client = DiscordClient(webhook_url, username="Marketplace Scanner")
    
    def send(self, data: MatchedListings) -> None:
        """
        Send matched listings data to Discord.
        Each listing will be sent as an individual embed with image, title, and price.
        
        Args:
            data (MatchedListings): The matched listings data object
        """
        print("Sending Discord notification...")
        
        # Get listing count
        count = data.get_listing_count()
        
        if count > 0:
            # Send each listing as a separate embed with image, price and title
            for listing in data.listings:
                self.send_listing(listing)
                
            print(f"Discord notification sent! ({count} listings)")
        else:
            # Send a message when no listings are found
            self.client.send_info(
                title="Marketplace Scan Complete",
                description="No new listings were found that match your criteria."
            )
            print("Discord notification sent! (No listings found)")
    
    def send_listing(self, listing: Dict[str, str]) -> None:
        """
        Send a single listing to Discord with focus on image, title, and price.
        
        Args:
            listing (Dict[str, str]): Dictionary containing listing data
        """
        # Extract the listing data
        title = listing.get('title', 'No Title')
        price = listing.get('price', 0)
        img_url = listing.get('img', '')
        
        # Format price with currency symbol
        price_str = f"${price}" if isinstance(price, (int, float)) else str(price)
        
        # Create a field for the price
        fields = [
            {
                "name": "Price",
                "value": price_str,
                "inline": True
            }
        ]
        
        # Create embed with the listing image as the main image
        image_obj = {"url": img_url} if img_url else None
        
        # Send the embed with title, price, and image
        self.client.send_embed(
            title=title,
            description="New marketplace listing found!",
            color=5763719,  # Green
            fields=fields,
            image=image_obj
        )