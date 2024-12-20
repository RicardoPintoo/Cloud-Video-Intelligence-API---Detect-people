
from dotenv import load_dotenv
from google.cloud import videointelligence


def main():
    video_client = videointelligence.VideoIntelligenceServiceClient()
    features = [videointelligence.Feature.LABEL_DETECTION]

    operation = video_client.annotate_video(
        request={
            'features': features,
            'input_uri': 'gs://bucket_of_videos/cat.mp4'
        }
    )

    print('\nProcessing Video for label annotations... ')

    result = operation.result(timeout=180)

    if operation.done():
        print('\nFinished processing')

    #print(dir(result))

    segment_labels = result.annotation_results[0].segment_label_annotations

    for segment_label in segment_labels:
        print('Video label description {}'.format(segment_label.entity.description))

        for category_entity in segment_label.category_entities:
            print(
                '\tLabel category: {}'.format(category_entity.description)
            )
             
        for i, segment in enumerate(segment_label.segments):
            start_time = (
                segment.segment.start_time_offset.seconds
                + segment.segment.start_time_offset.microseconds / 1e6
            )
            end_time = (
                segment.segment.end_time_offset.seconds
                + segment.segment.end_time_offset.microseconds / 1e6
            )
            positions = '{}s to {}s'.format(start_time, end_time)
            confidence = segment.confidence
            print('\tSegment {}: {}'.format(i, positions))
            print('\tConfidence: {}'.format(confidence))
        print('\n')

if __name__ == '__main__':
    load_dotenv()
    main()
