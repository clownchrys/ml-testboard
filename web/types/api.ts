import type {
  NextApiRequest as _NextApiRequest,
  NextApiResponse as _NextApiResponse
} from 'next'

export interface NextApiRequest<B> extends Omit<_NextApiResponse<B>, "body"> {
  body: B
}

export type NextApiResponse<R> = _NextApiResponse<R>
