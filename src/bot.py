import yaml

from instapy import InstaPy


class Bot:
    def __init__(self):
        self.session = None

    @staticmethod
    def read_config(path):
        print("Reading configuration file...")
        with open(path, "r") as file:
            config = yaml.safe_load(file)
        return config

    def create_session(self, login, password):
        print("Creating session...")
        session = InstaPy(username=login, password=password)
        session.login()
        self.session = session

    def init_session(self, config):
        """
        Initializes the Instagram session

        :param config: dict -
        :return:
        """
        print("Initializing session...")

        # Set limits in likes and comments so the account does not get banned for being a bot
        self.session.set_quota_supervisor(enabled=True, peak_likes_daily=100, peak_likes_hourly=20,
                                          peak_comments_daily=100, peak_comments_hourly=20,
                                          peak_follows_daily=50, peak_follows_hourly=10)

        # Get individual config parts
        like_config = config.get("like")  # dict
        comment_config = config.get("comment")  # dict
        follow_config = config.get("follow")  # dict
        relationship_bounds_config = config.get("relationship_bounds")

        # Get hashtags
        tags_to_like = config.get("hashtags_to_like")
        excluded_tags = config.get("hashtags_to_dont_like")

        relationship_bounds_enabled = relationship_bounds_config.get("enabled")
        if relationship_bounds_enabled:
            max_followers = relationship_bounds_config.get("max_followers")
            self.session.set_relationship_bounds(enabled=True, max_followers=max_followers)

        likes_enabled = like_config.get("enabled")
        if likes_enabled:
            amount = like_config.get("amount")
            self.session.like_by_tags(tags_to_like, amount=amount)
            self.session.set_dont_like(excluded_tags)

        comments_enabled = comment_config.get("enabled")
        if comments_enabled:
            percentage = comment_config.get("percentage")
            comment = comment_config.get("comment")
            self.session.set_do_comments(True, percentage=percentage)
            self.session.set_comments(comment)

        follow_enabled = follow_config.get("enabled")
        if follow_enabled:
            percentage = follow_config.get("percentage")
            self.session.set_do_follow(True, percentage=percentage)

    def close_session(self):
        print("Closing session...")
        # This will close the session, save the logs, and prepare a report that can be seen in the console output
        self.session.end()


def main():
    bot = Bot()

    # Read the configuration file
    config = bot.read_config("../config.yml")

    # Assign config to variables for further use
    username = config.get("username")
    password = config.get("password")

    # Create session and initialize the session configuration
    bot.create_session(username, password)
    bot.init_session(config)

    # Close the Instagram session
    bot.close_session()


if __name__ == "__main__":
    main()
